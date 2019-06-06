import argparse
import sys
import typing as ty

import meeting_finder.core.command_line as cl
import meeting_finder.core.doodle_poll as dp
import meeting_finder.component.parameter_provider as pp


class Loader(pp.ParameterProvider):
    def __init__(self) -> None:
        self.opened_file = sys.stdin

    def set_opened_file(self, opened_file: ty.TextIO) -> None:
        self.opened_file = opened_file

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

    def __init__(self, loader: Loader) -> None:
        self.loader = loader

    def process(self, opened_file: ty.TextIO) -> None:
        self.loader.set_opened_file(opened_file)
