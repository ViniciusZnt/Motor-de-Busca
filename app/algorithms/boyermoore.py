from typing import List, Dict
from app.algorithms.base import SearchStrategy


class BoyerMoore(SearchStrategy):
    """Boyer-Moore — O(N/M) melhor caso (sublinear), bad-character heuristic."""

    def _bad_char_table(self, pattern: str) -> Dict[str, int]:
        return {ch: i for i, ch in enumerate(pattern)}

    def search(self, text: str, pattern: str) -> List[int]:
        n, m = len(text), len(pattern)
        if m == 0:
            return []

        bad = self._bad_char_table(pattern)
        positions = []
        s = 0

        while s <= n - m:
            j = m - 1
            while j >= 0 and pattern[j] == text[s + j]:
                j -= 1
            if j < 0:
                positions.append(s)
                s += m - bad.get(text[s + m], -1) if s + m < n else 1
            else:
                s += max(1, j - bad.get(text[s + j], -1))

        return positions
