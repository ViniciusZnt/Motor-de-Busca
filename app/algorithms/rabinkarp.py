from typing import List
from app.algorithms.base import SearchStrategy

BASE = 31
MOD = 10**9 + 7


class RabinKarp(SearchStrategy):
    """Rabin-Karp — O(N+M) esperado, usando hash rolante."""

    def search(self, text: str, pattern: str) -> List[int]:
        n, m = len(text), len(pattern)
        if m == 0 or m > n:
            return []

        positions = []
        pat_hash = win_hash = 0
        power = 1

        for i in range(m):
            pat_hash = (pat_hash * BASE + ord(pattern[i])) % MOD
            win_hash = (win_hash * BASE + ord(text[i])) % MOD
            if i > 0:
                power = (power * BASE) % MOD

        if win_hash == pat_hash and text[:m] == pattern:
            positions.append(0)

        for i in range(1, n - m + 1):
            win_hash = (win_hash - ord(text[i - 1]) * power % MOD + MOD) % MOD
            win_hash = (win_hash * BASE + ord(text[i + m - 1])) % MOD
            if win_hash == pat_hash and text[i:i + m] == pattern:
                positions.append(i)

        return positions
