import sys

import pytest

import meeting_finder.components.csv_doodle_poll as cdp
import meeting_finder.components.command_line as cl
import meeting_finder.functions.parse_doodle_poll_from_csv_str as csv_parser

@pytest.fixture
def dispatcher():
    return cl.Dispatcher()


@pytest.fixture
def csv_file_parameter_with_spy_loader(spy_loader):
    return cdp.CsvFileParameter(spy_loader)


@pytest.fixture
def spy_loader():
    class SpyCsvDoodlePollFileLoader:
        def __init__(self):
            self.opened_file = None

        def set_opened_file(self, f):
            self.opened_file = f

    return SpyCsvDoodlePollFileLoader()


def test_parse_doodle_poll_from_csv_str(csv_str):
    poll = csv_parser.parse_doodle_poll_from_csv_str(csv_str)
    assert len(poll.respondents) == 13
    assert poll.respondents == \
        ('*A', 'B', 'C', 'D', 'E', 'F', '*G', 'H', 'I', 'J', '*K', 'L', '*M')
    assert len(poll.datetimes) == 84
    assert len(poll.availabilities) == 13
    assert len(poll.availabilities[0]) == 84


def test_csv_file_parameter_deafults_to_stdin(
        csv_file_parameter_with_spy_loader,
        dispatcher
        ):
    spy_loader = csv_file_parameter_with_spy_loader.loader
    dispatcher.add_param(csv_file_parameter_with_spy_loader)
    dispatcher.dispatch([])
    assert spy_loader.opened_file == sys.stdin


def test_csv_file_parameter_with_file_path(
        csv_file_parameter_with_spy_loader,
        dispatcher,
        csv_file
        ):
    spy_loader = csv_file_parameter_with_spy_loader.loader
    dispatcher.add_param(csv_file_parameter_with_spy_loader)
    dispatcher.dispatch(['--file', str(csv_file)])
    assert hasattr(spy_loader.opened_file, 'read')


def test_loader(csv_file):
    loader = cdp.CsvDoodlePollFileLoader()
    loader.opened_file = open(csv_file, 'r')
    doodle_poll = loader.load()
    assert len(doodle_poll.respondents) == 13


def test_loader_get_command_line_parameters():
    loader = cdp.CsvDoodlePollFileLoader()
    params = loader.get_command_line_parameters()
    assert len(params) == 1
    assert isinstance(params[0], cdp.CsvFileParameter)


def test_loader_set_opened_file(csv_file):
    opened_file = open(csv_file, 'r')
    loader = cdp.CsvDoodlePollFileLoader()
    loader.set_opened_file(opened_file)
    assert loader.opened_file == opened_file
