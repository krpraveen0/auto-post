#!/usr/bin/env python3
"""Render a DOCX to PDF and PNG files for CI layout checks."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    if not args.docx.exists():
        raise FileNotFoundError(args.docx)
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    pdftoppm = shutil.which("pdftoppm")
    if not soffice:
        raise RuntimeError("LibreOffice is required to render DOCX files.")
    if not pdftoppm:
        raise RuntimeError("pdftoppm from poppler-utils is required to render PDF pages.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(args.output_dir), str(args.docx)])
    pdf_path = args.output_dir / f"{args.docx.stem}.pdf"
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"PDF render failed: {pdf_path}")
    run([pdftoppm, "-png", "-r", "144", str(pdf_path), str(args.output_dir / "page")])
    pngs = sorted(args.output_dir.glob("page-*.png"))
    if not pngs:
        raise RuntimeError("DOCX rendered to PDF but produced no PNG pages.")
    for png in pngs:
        if png.stat().st_size < 1024:
            raise RuntimeError(f"Rendered page looks invalid or empty: {png}")
    print(f"Rendered {args.docx} to {pdf_path} and {len(pngs)} PNG page(s).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
