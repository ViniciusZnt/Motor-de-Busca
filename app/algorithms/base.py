from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class SearchResult:
    positions: List[int]
    occurrences: int
    found: bool
    duration_ms: float
    n: int  # text length
    m: int  # pattern length

    @classmethod
    def empty(cls, n: int, m: int, duration_ms: float) -> "SearchResult":
        return cls(positions=[], occurrences=0, found=False, duration_ms=duration_ms, n=n, m=m)


class SearchStrategy(ABC):
    @abstractmethod
    def search(self, text: str, pattern: str) -> List[int]:
        """Return list of starting positions where pattern occurs in text."""
        ...

    def execute(self, text: str, pattern: str) -> SearchResult:
        import time
        n, m = len(text), len(pattern)
        start = time.perf_counter()
        positions = self.search(text, pattern)
        duration_ms = (time.perf_counter() - start) * 1000
        return SearchResult(
            positions=positions,
            occurrences=len(positions),
            found=len(positions) > 0,
            duration_ms=round(duration_ms, 3),
            n=n,
            m=m,
        )
