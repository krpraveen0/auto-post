"""Inspect prefill, decode, and KV-cache behavior in a tiny causal model."""

from __future__ import annotations

import argparse
import csv
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Cache:
    keys: np.ndarray
    values: np.ndarray


class TinyCausalModel:
    def __init__(self, vocab_size: int = 64, d_model: int = 32, seed: int = 7):
        rng = np.random.default_rng(seed)
        scale = 1 / np.sqrt(d_model)
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.embedding = rng.normal(0, scale, (vocab_size, d_model))
        self.wq = rng.normal(0, scale, (d_model, d_model))
        self.wk = rng.normal(0, scale, (d_model, d_model))
        self.wv = rng.normal(0, scale, (d_model, d_model))
        self.wo = rng.normal(0, scale, (d_model, vocab_size))

    @staticmethod
    def softmax(x: np.ndarray) -> np.ndarray:
        shifted = x - np.max(x, axis=-1, keepdims=True)
        exp = np.exp(shifted)
        return exp / exp.sum(axis=-1, keepdims=True)

    def project(self, token_ids: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        hidden = self.embedding[token_ids]
        return hidden @ self.wq, hidden @ self.wk, hidden @ self.wv

    def prefill(self, prompt: np.ndarray) -> tuple[np.ndarray, Cache]:
        queries, keys, values = self.project(prompt)
        scores = queries @ keys.T / np.sqrt(self.d_model)
        causal = np.triu(np.full(scores.shape, -np.inf), k=1)
        attention = self.softmax(scores + causal)
        hidden = attention @ values
        return hidden[-1] @ self.wo, Cache(keys=keys, values=values)

    def decode_one(self, token_id: int, cache: Cache) -> tuple[np.ndarray, Cache]:
        token = np.array([token_id], dtype=np.int64)
        query, new_key, new_value = self.project(token)
        keys = np.concatenate([cache.keys, new_key], axis=0)
        values = np.concatenate([cache.values, new_value], axis=0)
        attention = self.softmax(query @ keys.T / np.sqrt(self.d_model))
        logits = (attention @ values)[0] @ self.wo
        return logits, Cache(keys=keys, values=values)

    def next_logits_recompute(self, sequence: np.ndarray) -> np.ndarray:
        logits, _ = self.prefill(sequence)
        return logits


def greedy(logits: np.ndarray) -> int:
    return int(np.argmax(logits))


def assert_cache_equivalence() -> None:
    model = TinyCausalModel()
    sequence = np.array([2, 5, 9, 4], dtype=np.int64)
    first_logits, cache = model.prefill(sequence)
    next_token = greedy(first_logits)
    cached_logits, cache = model.decode_one(next_token, cache)
    extended = np.append(sequence, next_token)
    recomputed_logits = model.next_logits_recompute(extended)
    np.testing.assert_allclose(cached_logits, recomputed_logits, rtol=1e-12, atol=1e-12)
    print(f"cache_equivalence=PASS max_abs_error={np.max(np.abs(cached_logits-recomputed_logits)):.3e}")
    print(f"prompt_tokens={len(sequence)} cache_tokens_after_decode={len(cache.keys)}")


def timed_ms(fn, repeats: int = 7) -> float:
    samples = []
    for _ in range(repeats):
        start = time.perf_counter_ns()
        fn()
        samples.append((time.perf_counter_ns() - start) / 1_000_000)
    return float(np.median(samples))


def benchmark(output: Path) -> None:
    model = TinyCausalModel(d_model=64)
    rng = np.random.default_rng(11)
    rows: list[dict[str, int | float | str]] = []

    for prompt_length in (16, 64, 256, 1024):
        prompt = rng.integers(0, model.vocab_size, size=prompt_length)
        ms = timed_ms(lambda: model.prefill(prompt))
        rows.append({"experiment": "prefill", "prompt_tokens": prompt_length, "output_tokens": 0, "median_ms": round(ms, 4)})

    prompt = rng.integers(0, model.vocab_size, size=128)
    for output_length in (1, 8, 32, 64):
        def run_cached() -> None:
            logits, cache = model.prefill(prompt)
            token = greedy(logits)
            for _ in range(output_length):
                logits, cache = model.decode_one(token, cache)
                token = greedy(logits)

        ms = timed_ms(run_cached)
        rows.append({"experiment": "cached_generation", "prompt_tokens": len(prompt), "output_tokens": output_length, "median_ms": round(ms, 4)})

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"benchmark_rows={len(rows)} output={output}")


def cache_bytes(layers: int, tokens: int, kv_heads: int, head_dim: int, bytes_per_value: int) -> int:
    return 2 * layers * tokens * kv_heads * head_dim * bytes_per_value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", type=Path)
    args = parser.parse_args()
    assert_cache_equivalence()
    example = cache_bytes(layers=32, tokens=4096, kv_heads=32, head_dim=128, bytes_per_value=2)
    print(f"illustrative_kv_cache_gib={example / 1024**3:.2f}")
    if args.benchmark:
        benchmark(args.benchmark)


if __name__ == "__main__":
    main()
