import argparse
import sys
import typing as ty
import datetime

import meeting_finder.app_base as app_base
import meeting_finder.components.command_line_base as cl_base
import meeting_finder.core.doodle_poll as dp


class CsvDoodlePollFileLoader(app_base.Component):
    def __init__(self) -> None:
        self.opened_file = sys.stdin

    def set_opened_file(self, opened_file: ty.TextIO) -> None:
        self.opened_file = opened_file

    def load(self) -> dp.DoodlePoll:
        string = self.opened_file.read()
        return self.parse_doodle_poll_from_csv_str(string)

    @staticmethod
    def parse_doodle_poll_from_csv_str(csv_str: str) -> dp.DoodlePoll:
        data = [line.split(',') for line in csv_str.split('\n')]

        for i in range(2, len(data)):
            if data[i][0] != '':
                names_start_row = i
                break
        for i in range(len(data)-1, -1, -1):
            if data[i][0] == 'Count':
                names_end_row = i
                break
        names = [r[0] for r in data[names_start_row:names_end_row]]

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
            start_datetime = datetime.datetime.strptime(
                start_datetime_str, '%b %Y %a %d %I:%M %p')
            start_datetimes.append(start_datetime)

        m = [r[1:] for r in data[names_start_row:names_end_row]]
        m2: ty.List[ty.List[dp.Response]] = []
        for r in m:
            row: ty.List[dp.Response] = []
            for v in r:
                if v == 'OK':
                    row.append(dp.Response.YES)
                elif v == '(OK)':
                    row.append(dp.Response.IF_NEED_BE)
                else:
                    row.append(dp.Response.NO)
            m2.append(row)

        return dp.DoodlePoll(names, start_datetimes, m2)

    def get_command_line_parameters(self) -> ty.Iterable[cl_base.Parameter]:
        return [self.CsvFileParameter(self)]

    class CsvFileParameter(cl_base.Parameter):
        name = '--file'
        opts = {
            'help':
            '(default stdin) Path to CSV file containing DoodlePoll results.',

            'type': argparse.FileType('r'),

            'default': sys.stdin,
        }

        def __init__(self, loader: 'CsvDoodlePollFileLoader') -> None:
            self.loader = loader

        def process(self, opened_file: ty.TextIO) -> None:
            self.loader.set_opened_file(opened_file)
