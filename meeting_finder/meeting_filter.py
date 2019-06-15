from abc import (
    abstractmethod
)

from typing import (
    Iterable,
    List
)

from meeting_finder.command_line import (
    CompositeCommandLineParameterProvider,
    CommandLineParameterProvider,
    CommandLineParameter
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
        self.conditions: List[MeetingCondition] = conditions

    def filter_meetings(
            self, meetings: Iterable[Meeting]) -> Iterable[Meeting]:
        for cond in self.conditions:
            meetings = filter(cond, meetings)
        return meetings

    def get_command_line_parameters(self) -> Iterable[CommandLineParameter]:
        return []
