import argparse
import sys
import typing as ty

import meeting_finder.app_base as app_base
import meeting_finder.components.command_line_base as cl_base
import meeting_finder.data.doodle_poll as dp
import meeting_finder.functions.parse_doodle_poll_from_csv_str as parse_dp


class CsvDoodlePollFileLoader(app_base.Component):
    def __init__(self) -> None:
        self.opened_file = sys.stdin

    def set_opened_file(self, opened_file: ty.TextIO) -> None:
        self.opened_file = opened_file

    def load(self) -> dp.DoodlePoll:
        string = self.opened_file.read()
        return parse_dp.parse_doodle_poll_from_csv_str(string)

    def get_command_line_parameters(self) -> ty.Iterable[cl_base.Parameter]:
        return [CsvFileParameter(self)]


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
