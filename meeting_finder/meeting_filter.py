from abc import (
    abstractmethod
)

from typing import (
    Iterable,
    List
)

from meeting_finder.command_line import (
    CompositeCommandLineParameterProvider,
    CommandLineParameterProvider
)
from meeting_finder.meeting_generator import (
    Meeting
)


class MeetingCondition(CommandLineParameterProvider):
    @abstractmethod
    def __call__(self, meeting: Meeting) -> bool:
        return True


class MeetingFilter(CompositeCommandLineParameterProvider):
    def __init__(self, conditions: List[MeetingCondition]) -> None:
        super().__init__()
        self.conditions: List[MeetingCondition] = conditions

        for c in self.conditions:
            self.add_command_line_parameter_provider(c)

    def filter_meetings(
            self, meetings: Iterable[Meeting]) -> Iterable[Meeting]:
        for cond in self.conditions:
            meetings = filter(cond, meetings)
        return meetings
