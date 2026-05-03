from typing import List
from app.algorithms.base import SearchStrategy


class KMP(SearchStrategy):
    """Knuth-Morris-Pratt — O(N+M) garantido, com tabela de falhas."""

    def _build_failure_table(self, pattern: str) -> List[int]:
        m = len(pattern)
        fail = [0] * m
        k = 0
        for i in range(1, m):
            while k > 0 and pattern[k] != pattern[i]:
                k = fail[k - 1]
            if pattern[k] == pattern[i]:
                k += 1
            fail[i] = k
        return fail

    def search(self, text: str, pattern: str) -> List[int]:
        n, m = len(text), len(pattern)
        if m == 0:
            return []
        fail = self._build_failure_table(pattern)
        positions = []
        q = 0
        for i in range(n):
            while q > 0 and pattern[q] != text[i]:
                q = fail[q - 1]
            if pattern[q] == text[i]:
                q += 1
            if q == m:
                positions.append(i - m + 1)
                q = fail[q - 1]
        return positions
