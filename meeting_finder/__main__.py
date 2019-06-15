import sys
from typing import (
    List
)


from meeting_finder.app import (
    App
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
from meeting_finder.meeting_conditions import (
    MinStartCondition
)


def main(args: List[str]) -> None:
    app = App(
        CommandLineProcessor(),
        CsvDoodlePollFileLoader(),
        MeetingGenerator(),
        MeetingFilter([
            MinStartCondition()
        ])
    )
    app.run(args)


if __name__ == '__main__':
    main(sys.argv[1:])
