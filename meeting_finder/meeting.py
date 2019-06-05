'''Meetings provide summarized access to information about each possible
meeting from a DoodlePoll.'''

import datetime
import operator
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Tuple


MeetingDict = Dict[str, Any]
MeetingTuple = Tuple[str, Iterable[str], Iterable[str]]


class Meeting:
    def __init__(
            self,
            start: datetime.datetime,
            facilitators: Iterable[str],
            participants: Iterable[str]
            ) -> None:
        self.start = start
        self.start_hour_24 = start.hour
        self.weekday = start.weekday()
        self.facilitators = frozenset(facilitators)
        self.participants = frozenset(participants)


def from_dict(dict_: MeetingDict) -> Meeting:
    start = datetime.datetime.strptime(dict_['start'], '%b %Y %a %d %I:%M %p')
    facilitators = list(dict_['facilitators'])
    participants = list(dict_['participants'])
    return Meeting(start, facilitators, participants)


def from_dicts(dicts: Iterable[MeetingDict]) -> Iterable[Meeting]:
    for dict_ in dicts:
        yield from_dict(dict_)


def from_tuples(tuples: Iterable[MeetingTuple]) -> Iterable[Meeting]:
    for tuple_ in tuples:
        yield from_tuple(tuple_)


def from_tuple(tuple_: MeetingTuple) -> Meeting:
    d = {
        'start': tuple_[0],
        'facilitators': tuple_[1],
        'participants': tuple_[2]
    }
    return from_dict(d)


def filter_meetings(
        meetings: Iterable[Meeting],
        field: str,
        bin_relational_op: Callable[[Any, Any], bool],
        val: Any
        ) -> Iterable[Meeting]:
    if bin_relational_op is operator.contains:
        def reverse_contains(a: Any, b: Any) -> bool:
            return operator.contains(b, a)
        bin_relational_op = reverse_contains
    return filter(
        lambda m: bin_relational_op(getattr(m, field), val), meetings)
