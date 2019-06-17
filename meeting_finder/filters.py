from typing import (
    Dict,
    Tuple,
    Callable,
    Generic,
    Iterable,
    List,
    TypeVar
)


T = TypeVar('T')
Condition = Callable[[T], bool]


class Filter(Generic[T]):
    def __init__(self, conditions: Iterable[Condition[T]]) -> None:
        self.conditions = list(conditions)

    def filter(self, ts: Iterable[T]) -> Iterable[T]:
        for c in self.conditions:
            ts = filter(c, ts)
        return ts


class CountingCondition(Generic[T]):
    def __init__(self, c: Condition[T]) -> None:
        self.condition = c
        self.accepted = 0
        self.rejected = 0

    def __call__(self, t: T) -> bool:
        result = self.condition(t)
        if result:
            self.accepted += 1
        else:
            self.rejected += 1
        return result

    @property
    def processed(self) -> int:
        return self.accepted + self.rejected


class CountingFilter(Filter[T]):
    def __init__(self, conditions: Iterable[CountingCondition[T]]) -> None:
        self.counting_conditions: List[CountingCondition[T]]
        self.counting_conditions = list(conditions)
        super().__init__(self.counting_conditions)

    def statistics(self) -> Dict[str, Tuple[int, int]]:
        stats: Dict[str, Tuple[int, int]] = {}
        for c in self.counting_conditions:
            stats[str([c])] = (c.accepted, c.rejected)
        return stats
