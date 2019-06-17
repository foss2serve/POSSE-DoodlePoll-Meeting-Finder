import argparse
from datetime import (
    datetime
)
from enum import (
    Enum
)
import sys
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    TextIO
)

from meeting_finder.command_line import (
    CommandLineParameterProvider,
    CommandLineParameter
)


class Response(Enum):
    NO = 0
    YES = 1
    IF_NEED_BE = 2


class Respondent:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


class Participant(Respondent):
    pass


class Facilitator(Respondent):
    pass


class DoodlePoll:
    def __init__(
            self,
            respondents: Iterable[Respondent],
            datetimes: Iterable[datetime],
            availabilities: Iterable[Iterable[Response]]
            ) -> None:
        self.respondents = tuple(respondents)
        self.datetimes = tuple(datetimes)
        self.availabilities = tuple(tuple(r) for r in availabilities)


class CsvDoodlePollFileLoader(CommandLineParameterProvider):
    def __init__(self) -> None:
        self.opened_file = sys.stdin

    def set_opened_file(self, opened_file: TextIO) -> None:
        self.opened_file = opened_file

    def load_doodle_poll(self) -> DoodlePoll:
        string = self.opened_file.read()
        return parse_doodle_poll_from_csv_str(string)

    def get_command_line_parameters(self) -> Iterable[CommandLineParameter]:
        return [CsvFileParameter(self)]


class CsvFileParameter(CommandLineParameter):
    def __init__(self, loader: CsvDoodlePollFileLoader) -> None:
        self.loader = loader

    def get_command_line_parameter_dest(self) -> str:
        return 'csv_file'

    def get_command_line_name_or_flags(self) -> Iterable[str]:
        return ['-f', '--csv-file']

    def get_command_line_options(self) -> Dict[str, Any]:
        return {
            'help':
            '(default stdin) Path to CSV file containing DoodlePoll results.',
            'type': argparse.FileType('r'),
            'default': sys.stdin,
        }

    def process_command_line_argument(self, opened_file: TextIO) -> None:
        self.loader.set_opened_file(opened_file)


def parse_doodle_poll_from_csv_str(csv_str: str) -> DoodlePoll:
    data = [line.split(',') for line in csv_str.split('\n')]

    for i in range(2, len(data)):
        if data[i][0] != '':
            names_start_row = i
            break
    for i in range(len(data)-1, -1, -1):
        if data[i][0] == 'Count':
            names_end_row = i
            break
    ns = [r[0] for r in data[names_start_row:names_end_row]]

    names: List[Respondent] = []
    for n in ns:
        if n[0] == '*':
            names.append(Facilitator(n))
        else:
            names.append(Participant(n))

    start_datetimes = []
    month_year_row = names_start_row - 3
    day_date_row = names_start_row - 2
    start_stop_row = names_start_row - 1
    for i in range(1, len(data[month_year_row])):
        if data[month_year_row][i] != '':
            month_year = data[month_year_row][i]
        if data[day_date_row][i] != '':
            day_date = data[day_date_row][i]
        start_stop = data[start_stop_row][i]
        start = start_stop.split(' – ')[0]
        start_datetime_str = ' '.join([month_year, day_date, start])
        start_datetime = datetime.strptime(
            start_datetime_str, '%B %Y %a %d %I:%M %p')
        start_datetimes.append(start_datetime)

    m = [r[1:] for r in data[names_start_row:names_end_row]]
    m2: List[List[Response]] = []
    for r in m:
        row: List[Response] = []
        for v in r:
            if v == 'OK':
                row.append(Response.YES)
            elif v == '(OK)':
                row.append(Response.IF_NEED_BE)
            else:
                row.append(Response.NO)
        m2.append(row)

    return DoodlePoll(names, start_datetimes, m2)
