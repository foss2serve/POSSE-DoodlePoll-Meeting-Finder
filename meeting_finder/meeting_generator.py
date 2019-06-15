from datetime import (
    datetime
)
from typing import (
    Any,
    Dict,
    Iterable,
    List
)

from meeting_finder.command_line import (
    CommandLineParameterProvider,
    CommandLineParameter
)
from meeting_finder.csv_doodle_poll import (
    DoodlePoll,
    Response
)


class Meeting:
    def __init__(
        self,
        start: datetime,
        facilitators: Iterable[str],
        participants: Iterable[str]
    ) -> None:
        self.start = start
        self.start_hour_24 = start.hour
        self.weekday = start.weekday()
        self.facilitators = frozenset(facilitators)
        self.participants = frozenset(participants)


class MeetingGenerator(CommandLineParameterProvider):
    def __init__(self) -> None:
        self.treat_if_need_be_as_yes = True

    def generate_meetings(self, poll: DoodlePoll) -> Iterable[Meeting]:
        return generate_meetings_from_doodle_poll(
            poll, self.treat_if_need_be_as_yes)

    def get_command_line_parameters(self) -> Iterable[CommandLineParameter]:
        return [TreatIfNeedBeAsNoParameter(self)]


class TreatIfNeedBeAsNoParameter(CommandLineParameter):
    def __init__(self, generator: MeetingGenerator) -> None:
        self.generator = generator

    def get_command_line_parameter_dest(self) -> str:
        return 'treat_if_need_be_as_no'

    def get_command_line_name_or_flags(self) -> Iterable[str]:
        return ['--treat-if-need-be-as-no']

    def get_command_line_options(self) -> Dict[str, Any]:
        return {
            'help': 'If set, treat "if-need-be" responses as "no" responses.',
            'action': 'store_true',
        }

    def process_command_line_argument(self, argument: bool) -> None:
        self.generator.treat_if_need_be_as_yes = False


def generate_meetings_from_doodle_poll(
    poll: DoodlePoll,
    treat_if_need_be_as_yes: bool
) -> Iterable[Meeting]:
    ms = []

    def is_yes(r: Response) -> bool:
        YES = Response.YES
        IF_NEED_BE = Response.IF_NEED_BE
        return r is YES or (treat_if_need_be_as_yes and r is IF_NEED_BE)

    def is_facilitator(name: str) -> bool:
        return name[0] == '*'

    for col, dt in enumerate(poll.datetimes):
        facilitators: List[str] = []
        participants: List[str] = []
        for row, name in enumerate(poll.respondents):
            if is_yes(poll.availabilities[row][col]):
                if is_facilitator(name):
                    facilitators.append(name)
                else:
                    participants.append(name)
        m = Meeting(dt, facilitators, participants)
        ms.append(m)
    return ms
