import unittest

import numpy as np

from one_token import Cache, TinyCausalModel, cache_bytes, greedy


class TinyCausalModelTests(unittest.TestCase):
    def test_cached_decode_matches_full_recomputation(self):
        model = TinyCausalModel()
        prompt = np.array([1, 3, 5, 7], dtype=np.int64)
        logits, cache = model.prefill(prompt)
        token = greedy(logits)
        cached, updated = model.decode_one(token, cache)
        recomputed = model.next_logits_recompute(np.append(prompt, token))
        np.testing.assert_allclose(cached, recomputed, rtol=1e-12, atol=1e-12)
        self.assertEqual(updated.keys.shape, (5, model.d_model))

    def test_cache_memory_formula_counts_keys_and_values(self):
        self.assertEqual(cache_bytes(2, 10, 4, 8, 2), 2560)

    def test_failure_fixture_rejects_corrupted_cache(self):
        model = TinyCausalModel()
        prompt = np.array([1, 2, 3], dtype=np.int64)
        logits, cache = model.prefill(prompt)
        token = greedy(logits)
        corrupted = Cache(keys=cache.keys, values=np.zeros_like(cache.values))
        cached, _ = model.decode_one(token, corrupted)
        recomputed = model.next_logits_recompute(np.append(prompt, token))
        with self.assertRaises(AssertionError):
            np.testing.assert_allclose(cached, recomputed, rtol=1e-12, atol=1e-12)


if __name__ == "__main__":
    unittest.main()
