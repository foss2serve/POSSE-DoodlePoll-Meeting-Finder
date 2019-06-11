'''
Meeting provide summarized access to information about each possible
meeting from a DoodlePoll.
'''

import datetime
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
