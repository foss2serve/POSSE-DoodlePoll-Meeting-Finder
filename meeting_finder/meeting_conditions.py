from abc import (
    abstractmethod
)
from typing import (
    Any,
    Dict,
    Iterable
)

from meeting_finder.command_line import (
    CommandLineParameter
)
from meeting_finder.meeting_filter import (
    MeetingCondition
)
from meeting_finder.meeting_generator import (
    Meeting
)


class CommandLineControlledMeetingCondition(
    MeetingCondition, CommandLineParameter
):
    @abstractmethod
    def get_command_line_parameter_dest(self) -> str:
        return ''

    @abstractmethod
    def get_command_line_name_or_flags(self) -> Iterable[str]:
        return ['']

    @abstractmethod
    def get_command_line_options(self) -> Dict[str, Any]:
        return {}

    @abstractmethod
    def process_command_line_argument(self, argument: Any) -> None:
        pass

    @abstractmethod
    def __call__(self, meeting: Meeting) -> bool:
        return True


class MinStartCondition(CommandLineControlledMeetingCondition):
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

    def __call__(self, meeting: Meeting) -> bool:
        return meeting.start_hour_24 >= self.threshold


class MaxStartCondition(CommandLineControlledMeetingCondition):
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

    def __call__(self, meeting: Meeting) -> bool:
        return meeting.start_hour_24 <= self.threshold
