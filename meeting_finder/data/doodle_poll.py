import datetime
import enum
import typing as ty


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
