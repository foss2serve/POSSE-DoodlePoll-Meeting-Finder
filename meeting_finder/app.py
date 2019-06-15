from typing import (
    List
)

from meeting_finder.command_line import (
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


class App:
    def __init__(
            self,
            command_line_processor: CommandLineProcessor,
            csv_doodle_poll_file_loader: CsvDoodlePollFileLoader,
            meeting_generator: MeetingGenerator,
            meeting_filter: MeetingFilter
            ) -> None:

        self.command_line_processor = command_line_processor
        self.csv_doodle_poll_file_loader = csv_doodle_poll_file_loader
        self.meeting_generator = meeting_generator
        self.meeting_filter = meeting_filter

        self.command_line_processor.add_all_command_line_parameter_providers([
            self.csv_doodle_poll_file_loader,
            self.meeting_generator,
            self.meeting_filter,
        ])

    def run(self, args: List[str]) -> None:
        self.command_line_processor.process_command_line_arguments(args)
        doodle_poll = self.csv_doodle_poll_file_loader.load_doodle_poll()
        meetings = self.meeting_generator.generate_meetings(doodle_poll)
        meetings = self.meeting_filter.filter_meetings(meetings)
        print(meetings)
