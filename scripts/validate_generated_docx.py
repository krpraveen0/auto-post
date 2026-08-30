#!/usr/bin/env python3
"""Validate generated Medium DOCX artifacts and optionally render them."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


REQUIRED_DOCX_MEMBERS = {
    "[Content_Types].xml",
    "_rels/.rels",
    "word/document.xml",
}


def find_docx_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.docx") if path.is_file())


def validate_docx_archive(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.stat().st_size == 0:
        raise RuntimeError(f"DOCX is empty: {path}")
    if not zipfile.is_zipfile(path):
        raise RuntimeError(f"DOCX is not a valid zip archive: {path}")
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        missing = REQUIRED_DOCX_MEMBERS - names
        if missing:
            raise RuntimeError(f"DOCX is missing required members: {path}: {sorted(missing)}")
        document_xml = archive.read("word/document.xml")
        if b"<w:body" not in document_xml:
            raise RuntimeError(f"DOCX document body is missing: {path}")


def render_docx(path: Path, output_root: Path) -> None:
    if not shutil.which("soffice") and not shutil.which("libreoffice"):
        raise RuntimeError("LibreOffice is required for DOCX rendering.")
    if not shutil.which("pdftoppm"):
        raise RuntimeError("pdftoppm from poppler-utils is required for DOCX rendering.")
    output_dir = output_root / path.stem
    subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("render_docx_ci.py")),
            str(path),
            "--output-dir",
            str(output_dir),
        ],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="medium/generated", type=Path)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--render-output-dir", default="medium/generated/rendered-validation", type=Path)
    args = parser.parse_args()

    docx_files = find_docx_files(args.root)
    if not docx_files:
        print(f"No generated DOCX files found under {args.root}.")
        return 0

    for docx in docx_files:
        validate_docx_archive(docx)
        print(f"Validated DOCX archive: {docx}")
        if args.render:
            render_docx(docx, args.render_output_dir)

    print(f"Validated {len(docx_files)} DOCX file(s).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
