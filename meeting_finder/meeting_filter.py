from abc import (
    abstractmethod
)
from typing import (
    Any,
    Dict,
    Iterable
)


from meeting_finder.command_line import (
    CompositeCommandLineParameterProvider,
    CommandLineParameter
)
from meeting_finder.meeting_generator import (
    Meeting
)
from meeting_finder.filters import (
    CountingFilter,
    CountingCondition
)


class MeetingFilter(
        CountingFilter[Meeting],
        CompositeCommandLineParameterProvider):
    '''A command-line-controlled, counting-filter for meetings.'''
    pass


class MeetingCondition(
        CountingCondition[Meeting],
        CommandLineParameter):
    '''A command-line-controlled, couting-condition for meetings.

    Each subclass is controlled by a command-line option that it describes
    by implementing the abstract methods of CommandLineParameter. Each subclass
    also implmenets an abstract condition method which is used to filter
    Meetings.
    '''

    def __init__(self) -> None:
        super().__init__(self.condition)

    @abstractmethod
    def condition(self, m: Meeting) -> bool:
        return True


class MinStartCondition(MeetingCondition):
    def get_command_line_parameter_dest(self) -> str:
        return 'min_start'

    def get_command_line_name_or_flags(self) -> Iterable[str]:
        return ['-s', '--min-start']

    def get_command_line_options(self) -> Dict[str, Any]:
        return {
            'help': '-s=14 means meetings must start 2pm or later.',
            'type': int,
            'default': 0,
        }

    def process_command_line_argument(self, argument: int) -> None:
        self.threshold = argument

    def condition(self, meeting: Meeting) -> bool:
        return meeting.start_hour_24 >= self.threshold


class MaxStartCondition(MeetingCondition):
    def get_command_line_parameter_dest(self) -> str:
        return 'max_start'

    def get_command_line_name_or_flags(self) -> Iterable[str]:
        return ['-S', '--max-start']

    def get_command_line_options(self) -> Dict[str, Any]:
        return {
            'help': '-S=14 means meetings must start 2pm or earlier.',
            'type': int,
            'default': 23,
        }

    def process_command_line_argument(self, argument: int) -> None:
        self.threshold = argument

    def condition(self, meeting: Meeting) -> bool:
        return meeting.start_hour_24 <= self.threshold
