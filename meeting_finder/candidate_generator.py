from typing import (
    Any,
    Dict,
    Iterable
)

from meeting_finder.command_line import (
    CommandLineParameter
)
from meeting_finder.meeting_generator import (
    Meeting
)
from meeting_finder.csv_doodle_poll import (
    Facilitator,
    Participant
)


class Candidate:
    def __init__(
            self,
            meetings: Iterable[Meeting],
            participants: Iterable[Participant],
            facilitators: Iterable[Facilitator]) -> None:
        self.meetings = list(meetings)
        self.participants = list(participants)
        self.facilitators = list(facilitators)


class CandidateGenerator(CommandLineParameter):
    def get_command_line_parameter_dest(self) -> str:
        return 'meetings_per_solution'

    def get_command_line_name_or_flags(self) -> Iterable[str]:
        return ['-m', '--meetings_per_solution']

    def get_command_line_options(self) -> Dict[str, Any]:
        return {
            'help': 'Each solution must have exactly this many meetings',
            'type': int,
            'default': 1,
        }

    def process_command_line_argument(self, argument: int) -> None:
        self.meetings_per_solution = argument

    def generate_candidates(
            self,
            meetings: Iterable[Meeting]) -> Iterable[Candidate]:
        return []

    def number_of_candidates(self, number_of_meetings: int) -> int:
        # TODO: nCr
        return 0
