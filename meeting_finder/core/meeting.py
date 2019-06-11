'''
Meeting provide summarized access to information about each possible
meeting from a DoodlePoll.
'''

import datetime
import operator
import typing as ty


class Meeting:
    def __init__(
            self,
            start: datetime.datetime,
            facilitators: ty.Iterable[str],
            participants: ty.Iterable[str]
            ) -> None:
        self.start = start
        self.start_hour_24 = start.hour
        self.weekday = start.weekday()
        self.facilitators = frozenset(facilitators)
        self.participants = frozenset(participants)


# I suspect the rest of this won't be used by any part of the system except
# for tests. If so, it should be moved to a test helper.

MeetingDict = ty.Dict[str, ty.Any]
MeetingTuple = ty.Tuple[str, ty.Iterable[str], ty.Iterable[str]]


def from_dict(dict_: MeetingDict) -> Meeting:
    start = datetime.datetime.strptime(dict_['start'], '%b %Y %a %d %I:%M %p')
    facilitators = list(dict_['facilitators'])
    participants = list(dict_['participants'])
    return Meeting(start, facilitators, participants)


def from_dicts(dicts: ty.Iterable[MeetingDict]) -> ty.Iterable[Meeting]:
    for dict_ in dicts:
        yield from_dict(dict_)


def from_tuples(tuples: ty.Iterable[MeetingTuple]) -> ty.Iterable[Meeting]:
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
        meetings: ty.Iterable[Meeting],
        field: str,
        bin_relational_op: ty.Callable[[ty.Any, ty.Any], bool],
        val: ty.Any
        ) -> ty.Iterable[Meeting]:
    if bin_relational_op is operator.contains:
        def reverse_contains(a: ty.Any, b: ty.Any) -> bool:
            return operator.contains(b, a)
        bin_relational_op = reverse_contains
    return filter(
        lambda m: bin_relational_op(getattr(m, field), val), meetings)
