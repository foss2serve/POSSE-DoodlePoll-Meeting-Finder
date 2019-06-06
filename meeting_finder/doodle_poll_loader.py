import argparse
import sys
import typing as ty

import meeting_finder.command_line as cl
import meeting_finder.doodle_poll as dp


class DoodlePollLoader(cl.ParameterProvider):
    def __init__(self) -> None:
        self.opened_file = sys.stdin

    def load(self) -> dp.DoodlePoll:
        string = self.opened_file.read()
        return dp.from_csv_str(string)

    def get_command_line_parameters(self) -> ty.Iterable[cl.Parameter]:
        return [CsvFileParameter(self)]


class CsvFileParameter(cl.Parameter):
    name = '--file'
    opts = {
        'help':
            '(default stdin) Path to CSV file containing DoodlePoll results.',
        'type': argparse.FileType('r'),
        'default': sys.stdin,
    }

    def __init__(self, loader: DoodlePollLoader) -> None:
        self.loader = loader

    def process(self, opened_file: ty.TextIO) -> None:
        self.loader.opened_file = opened_file
