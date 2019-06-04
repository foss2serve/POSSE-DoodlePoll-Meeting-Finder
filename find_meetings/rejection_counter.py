from collections import defaultdict
from typing import Dict, Tuple, Iterable, List

from find_meetings.condition import Condition, Item


def wrap(
        conditions: Iterable[Condition[Item]]
        ) -> Tuple[List[Condition[Item]], Dict[str, int]]:
    wrapped: List[Condition[Item]] = []
    counts: Dict[str, int] = defaultdict(lambda: 0)
    for cond in conditions:
        w = RejectionCounter(counts, cond.name, cond)
        wrapped.append(w)
    return wrapped, counts


class RejectionCounter(Condition[Item]):
    '''
    Example:
    counts = defaultdict(lambda: 0)
    rc = RejectionCounter(counts, 'blah', lambda item: item < 3)
    list(filter(rc, [1, 2, 3, 4, 5, 6, 7]))
    assert counts['blah'] == 4, 'because 4 items were not less than 3.'
    '''
    def __init__(
            self,
            counts: Dict[str, int],
            name: str,
            condition: Condition[Item]
            ):
        self._counts = counts
        self._name = name
        self._condition = condition

    def __call__(self, item: Item) -> bool:
        result = self._condition(item)
        if not result:
            self._counts[self._name] += 1
        return result
