# Golden One-Token Experiment

This companion project exposes prefill, one-token decoding, and KV-cache reuse
in a deliberately small causal-attention model. It is a mechanism demonstration,
not a production GPU benchmark.

## Environment

- Python 3.12.13
- NumPy 2.1.3
- CPU execution

## Run

```bash
python -m pip install -r requirements.txt
python -m unittest -v
python one_token.py --benchmark results/benchmark.csv
```

Expected invariants:

- `cache_equivalence=PASS`
- maximum absolute error near floating-point precision
- cache length increases by one after one decode step
- three unit tests pass, including the corrupted-cache failure fixture

Timing values depend on the CPU, BLAS implementation, operating system, and
background load. Interpret their direction within one run; do not compare these
toy CPU values with production serving systems.
