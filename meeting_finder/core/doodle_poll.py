import datetime
import enum
import typing as ty

import meeting_finder.core.meeting as mtg


class Response(enum.Enum):
    NO = 0
    YES = 1
    IF_NEED_BE = 2


class DoodlePoll:
    def __init__(
            self,
            respondents: ty.Iterable[str],
            datetimes: ty.Iterable[datetime.datetime],
            availabilities: ty.Iterable[ty.Iterable[Response]]
            ) -> None:
        self.respondents = tuple(respondents)
        self.datetimes = tuple(datetimes)
        self.availabilities = tuple(tuple(r) for r in availabilities)

    def get_meetings(
            self,
            treat_if_need_be_as_yes: bool = True
            ) -> ty.Iterable[mtg.Meeting]:
        ms = []
        for col, dt in enumerate(self.datetimes):
            facilitators: ty.List[str] = []
            participants: ty.List[str] = []
            for row, name in enumerate(self.respondents):
                r = self.availabilities[row][col]
                if r is Response.YES \
                    or (treat_if_need_be_as_yes
                        and r is Response.IF_NEED_BE):
                    if name[0] == '*':
                        facilitators.append(name)
                    else:
                        participants.append(name)
            m = mtg.Meeting(dt, facilitators, participants)
            ms.append(m)
        return ms
