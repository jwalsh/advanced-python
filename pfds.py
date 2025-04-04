import heapq
from collections import deque
from typing import Any, Callable, List, Tuple


# Banker's Queue
class BankersQueue:
    def __init__(self, front: List[Any] = [], rear: List[Any] = []):
        self.front = front
        self.rear = rear

    def snoc(self, x: Any) -> "BankersQueue":
        return BankersQueue(self.front, [x] + self.rear)

    def head(self) -> Any:
        if not self.front:
            return BankersQueue(list(reversed(self.rear)), [])
        return self.front[-1]

    def tail(self) -> "BankersQueue":
        if not self.front:
            return BankersQueue(list(reversed(self.rear))[1:], [])
        return BankersQueue(self.front[:-1], self.rear)


# Skew Binary Random-Access List
class SkewBinaryList:
    def __init__(self, trees: List[Tuple[int, List[Any]]] = []):
        self.trees = trees

    def cons(self, x: Any) -> "SkewBinaryList":
        if len(self.trees) >= 2 and self.trees[0][0] == self.trees[1][0]:
            t1, t2, *rest = self.trees
            return SkewBinaryList([(1 + t1[0] + t2[0], [x, t1[1], t2[1]])] + rest)
        return SkewBinaryList([(1, [x])] + self.trees)

    def head(self) -> Any:
        return self.trees[0][1][0]

    def tail(self) -> "SkewBinaryList":
        _, [_, *t], *ts = self.trees
        if t:
            return SkewBinaryList([(len(t), t)] + ts)
        return SkewBinaryList(ts)

    def lookup(self, i: int) -> Any:
        def look(i: int, trees: List[Tuple[int, List[Any]]]) -> Any:
            w, t, *ts = trees
            if i < w:
                return t[i]
            return look(i - w, ts)

        return look(i, self.trees)

    def update(self, i: int, y: Any) -> "SkewBinaryList":
        def upd(
            i: int, trees: List[Tuple[int, List[Any]]]
        ) -> List[Tuple[int, List[Any]]]:
            (w, t), *ts = trees
            if i < w:
                return [(w, [y if j == i else x for j, x in enumerate(t)])] + ts
            return [(w, t)] + upd(i - w, ts)

        return SkewBinaryList(upd(i, self.trees))


# Skew Binomial Heap
class SkewBinomialHeap:
    def __init__(self, trees: List[Tuple[int, Any, List["SkewBinomialHeap"]]] = []):
        self.trees = trees

    def insert(self, x: Any) -> "SkewBinomialHeap":
        def ins(ts):
            if len(ts) >= 2 and ts[0][0] == ts[1][0]:
                t1, t2, *rest = ts
                return [
                    (
                        1 + t1[0] + t2[0],
                        min(x, t1[1], t2[1]),
                        [SkewBinomialHeap([t1]), SkewBinomialHeap([t2])],
                    )
                ] + rest
            return [(1, x, [])] + ts

        return SkewBinomialHeap(ins(self.trees))

    def find_min(self) -> Any:
        return min(t[1] for t in self.trees)

    def delete_min(self) -> "SkewBinomialHeap":
        def merge(h1: "SkewBinomialHeap", h2: "SkewBinomialHeap") -> "SkewBinomialHeap":
            if not h1.trees:
                return h2
            if not h2.trees:
                return h1
            if h1.trees[0][0] < h2.trees[0][0]:
                return SkewBinomialHeap(
                    [h1.trees[0]] + merge(SkewBinomialHeap(h1.trees[1:]), h2).trees
                )
            if h2.trees[0][0] < h1.trees[0][0]:
                return SkewBinomialHeap(
                    [h2.trees[0]] + merge(h1, SkewBinomialHeap(h2.trees[1:])).trees
                )
            return merge(
                SkewBinomialHeap(h1.trees[1:]), SkewBinomialHeap(h2.trees[1:])
            ).insert(min(h1.trees[0][1], h2.trees[0][1]))

        _, x, ts = min(self.trees, key=lambda t: t[1])
        return merge(
            SkewBinomialHeap(self.trees[1:]), SkewBinomialHeap([t for _, _, t in ts])
        )


# Sortable Collection
class SortableCollection:
    def __init__(
        self,
        elements: List[Any] = [],
        compare: Callable[[Any, Any], int] = lambda x, y: x - y,
    ):
        self.elements = elements
        self.compare = compare

    def add(self, x: Any) -> "SortableCollection":
        return SortableCollection(self.elements + [x], self.compare)

    def sort(self) -> List[Any]:
        return sorted(self.elements, key=functools.cmp_to_key(self.compare))
