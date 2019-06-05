import argparse
import sys

import find_meetings.command_line as command_line
import find_meetings.doodle_poll as doodle_poll


class DoodlePollLoader:
    def __init__(self):
        self.opened_file = None

    def get_command_line_params(self):
        return [CsvFileParamter(self)]

    def load(self):
        csv_string = self.opened_file.read()
        self.opened_file.close()
        return doodle_poll.from_csv_str(csv_string)


class CsvFileParameter(command_line.Parameter):
    name = '--csv-file':
    opts = {
        'type': argparse.FileType('r')
        'default': sys.stdin
    }
    def __init__(self, loader):
        self.loader = loader

    def process(self, param, arg):
        self.loader.opend_file = arg
