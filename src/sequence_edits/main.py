from typing import Iterable, TypeVar
import ramda as R
from .edits import Skip, Insert, Inserted

V =  TypeVar("V")    
def decompress(edits: list[Skip|Insert[V]], start: int, end: int) -> Iterable[int|Inserted[V]]:
    """Applies `edits` to `[start, end)`, returning a full iterable of indices
    - e.g. `decompress([insert(4), skip(6)], start=3, end=8) == xs `
        - `list(xs) == [3, None, 4, 5, 7] # inserted before 4, skipped 6`
    """
    i = start
    for edit in filter(lambda e: start <= e.idx < end, edits):
        yield from range(i, edit.idx)
        if edit.type == "skip":
            i = edit.idx+1
        elif edit.type == "insert":
            yield Inserted(edit.value)
            i = edit.idx
    yield from range(i, end)

A = TypeVar('A')
def apply(edits: list[Skip|Insert[V]], xs: list[A], start: int = 0) -> Iterable[A | V]:
    """Applies `edits` to an actual list `xs[start:]`"""
    for i in decompress(edits, start=start, end=len(xs)):
        yield i.value if isinstance(i, Inserted) else xs[i]