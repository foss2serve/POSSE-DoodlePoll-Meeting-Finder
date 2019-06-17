import sys

from typing import (
    Any,
    Dict,
    Iterable,
    List
)

from meeting_finder.command_line import (
    CommandLineParameter,
    CommandLineParameterProvider,
    CommandLineProcessor
)
from meeting_finder.csv_doodle_poll import (
    CsvDoodlePollFileLoader
)
from meeting_finder.meeting_generator import (
    MeetingGenerator
)
from meeting_finder.meeting_filter import (
    MeetingFilter
)
from meeting_finder.candidate_generator import (
    CandidateGenerator
)


class App(CommandLineParameterProvider):
    def __init__(
            self,
            command_line_processor: CommandLineProcessor,
            csv_doodle_poll_file_loader: CsvDoodlePollFileLoader,
            meeting_generator: MeetingGenerator,
            meeting_filter: MeetingFilter,
            candidate_generator: CandidateGenerator
            ) -> None:
        self.dry_run = False

        self.command_line_processor = command_line_processor
        self.csv_doodle_poll_file_loader = csv_doodle_poll_file_loader
        self.meeting_generator = meeting_generator
        self.meeting_filter = meeting_filter
        self.candidate_generator = candidate_generator

        self.command_line_processor.add_all_command_line_parameter_providers([
            self.csv_doodle_poll_file_loader,
            self.meeting_generator,
            self.meeting_filter,
            self,
            self.candidate_generator,
        ])

    def run(self, args: List[str]) -> None:
        self.command_line_processor.process_command_line_arguments(args)
        doodle_poll = self.csv_doodle_poll_file_loader.load_doodle_poll()
        meetings = self.meeting_generator.generate_meetings(doodle_poll)
        meetings = self.meeting_filter.filter(meetings)
        meetings = list(meetings)
        print(self.meeting_filter.statistics())
        print(self.candidate_generator.number_of_candidates(len(meetings)))
        if self.dry_run:
            sys.exit(0)
        candidates = self.candidate_generator.generate_candidates(meetings)
        print(candidates)

    def get_command_line_parameters(self) -> Iterable[CommandLineParameter]:
        return [DryRunParameter(self)]


class DryRunParameter(CommandLineParameter):
    def __init__(self, app: App) -> None:
        self.app = app

    def get_command_line_parameter_dest(self) -> str:
        return 'dry_run'

    def get_command_line_name_or_flags(self) -> Iterable[str]:
        return ['-d', '--dry-run']

    def get_command_line_options(self) -> Dict[str, Any]:
        return {
            'help': 'If set, report statistics and exit.',
            'type': bool,
            'action': 'store_true',
        }

    def process_command_line_argument(self, argument: Any) -> None:
        self.app.dry_run = True
