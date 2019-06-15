import sys

import pytest

from meeting_finder.csv_doodle_poll import (
    CsvFileParameter,
    CsvDoodlePollFileLoader,
    parse_doodle_poll_from_csv_str
)
from meeting_finder.command_line import (
    CommandLineProcessor
)


@pytest.fixture
def command_line_processor():
    return CommandLineProcessor()


@pytest.fixture
def csv_file_parameter_with_spy_loader(spy_loader):
    return CsvFileParameter(spy_loader)


@pytest.fixture
def spy_loader():
    class SpyCsvDoodlePollFileLoader:
        def __init__(self):
            self.opened_file = None

        def set_opened_file(self, f):
            self.opened_file = f

    return SpyCsvDoodlePollFileLoader()


def test_parse_doodle_poll_from_csv_str(csv_str):
    poll = parse_doodle_poll_from_csv_str(csv_str)
    assert len(poll.respondents) == 13
    assert poll.respondents == \
        ('*A', 'B', 'C', 'D', 'E', 'F', '*G', 'H', 'I', 'J', '*K', 'L', '*M')
    assert len(poll.datetimes) == 84
    assert len(poll.availabilities) == 13
    assert len(poll.availabilities[0]) == 84


def test_csv_file_parameter_deafults_to_stdin(
        csv_file_parameter_with_spy_loader,
        command_line_processor
        ):
    spy_loader = csv_file_parameter_with_spy_loader.loader
    command_line_processor.add_command_line_parameter_provider(csv_file_parameter_with_spy_loader)
    command_line_processor.process_command_line_arguments([])
    assert spy_loader.opened_file == sys.stdin


def test_csv_file_parameter_with_file_path(
        csv_file_parameter_with_spy_loader,
        command_line_processor,
        csv_file
        ):
    spy_loader = csv_file_parameter_with_spy_loader.loader
    command_line_processor.add_command_line_parameter_provider(csv_file_parameter_with_spy_loader)
    command_line_processor.process_command_line_arguments(['--csv-file', str(csv_file)])
    assert hasattr(spy_loader.opened_file, 'read')


def test_loader(csv_file):
    loader = CsvDoodlePollFileLoader()
    loader.opened_file = open(csv_file, 'r')
    doodle_poll = loader.load_doodle_poll()
    assert len(doodle_poll.respondents) == 13


def test_loader_get_command_line_parameters():
    loader = CsvDoodlePollFileLoader()
    params = loader.get_command_line_parameters()
    assert len(params) == 1
    assert isinstance(params[0], CsvFileParameter)


def test_loader_set_opened_file(csv_file):
    opened_file = open(csv_file, 'r')
    loader = CsvDoodlePollFileLoader()
    loader.set_opened_file(opened_file)
    assert loader.opened_file == opened_file
