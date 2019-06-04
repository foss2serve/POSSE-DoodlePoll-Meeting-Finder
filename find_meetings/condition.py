from abc import abstractmethod
from typing import TypeVar, Generic, Iterable, Dict, Any, List

from find_meetings.meeting import Meeting


Item = TypeVar('Item')


def filter_items(
        items: Iterable[Item],
        conditions: Iterable['Condition[Item]']
        ) -> Iterable[Item]:
    for cond in conditions:
        items = filter(cond, items)
    return list(items)


def get_conditions(spec: Dict[str, Any]) -> List['Condition[Meeting]']:
    conditions = []
    for name, value in spec.items():
        conditions.append(globals()[name](value))
    return conditions


class Condition(Generic[Item]):
    def __init__(self) -> None:
        self.name = type(self).__name__

    @abstractmethod
    def __call__(self, item: Item) -> bool:
        return True


class IntCondition(Condition[Item]):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class Days(Condition[Meeting]):
    def __init__(self, value: Iterable[int]) -> None:
        super().__init__()
        self.value = value

    def __call__(self, meeting: Meeting) -> bool:
        return meeting.weekday in self.value


class MinStart(IntCondition[Meeting]):
    def __call__(self, meeting: Meeting) -> bool:
        return meeting.hour >= self.value


class MaxStart(IntCondition[Meeting]):
    def __call__(self, meeting: Meeting) -> bool:
        return meeting.hour <= self.value


class MinFacilitators(IntCondition[Meeting]):
    def __call__(self, meeting: Meeting) -> bool:
        return len(meeting.facilitators) >= self.value


class MaxFacilitators(IntCondition[Meeting]):
    def __call__(self, meeting: Meeting) -> bool:
        return len(meeting.facilitators) <= self.value


class MinParticipants(IntCondition[Meeting]):
    def __call__(self, meeting: Meeting) -> bool:
        return len(meeting.participants) >= self.value


class MaxParticipants(IntCondition[Meeting]):
    def __call__(self, meeting: Meeting) -> bool:
        return len(meeting.participants) <= self.value


class MinPeople(IntCondition[Meeting]):
    def __call__(self, meeting: Meeting) -> bool:
        return len(meeting.facilitators | meeting.participants) >= self.value


class MaxPeople(IntCondition[Meeting]):
    def __call__(self, meeting: Meeting) -> bool:
        return len(meeting.facilitators | meeting.participants) <= self.value
