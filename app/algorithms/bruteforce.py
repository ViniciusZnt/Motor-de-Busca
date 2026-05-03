from typing import List
from app.algorithms.base import SearchStrategy


class BruteForce(SearchStrategy):
    """Força Bruta (Naive) — O(N·M) pior caso."""

    def search(self, text: str, pattern: str) -> List[int]:
        n, m = len(text), len(pattern)
        positions = []
        for i in range(n - m + 1):
            j = 0
            while j < m and text[i + j] == pattern[j]:
                j += 1
            if j == m:
                positions.append(i)
        return positions
