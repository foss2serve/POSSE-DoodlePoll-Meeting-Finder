import sys

import pytest

import meeting_finder.core.doodle_poll as dp
import meeting_finder.core.command_line as cl
import meeting_finder.component.doodle_poll_csv_loader as dpcl


def test_from_csv_str(csv_str):
    poll = dp.from_csv_str(csv_str)
    assert len(poll.respondents) == 13
    assert poll.respondents == \
        ('*A', 'B', 'C', 'D', 'E', 'F', '*G', 'H', 'I', 'J', '*K', 'L', '*M')
    assert len(poll.datetimes) == 84
    assert len(poll.availabilities) == 13
    assert len(poll.availabilities[0]) == 84


def test_get_meetings(csv_str):
    poll = dp.from_csv_str(csv_str)
    ms = poll.get_meetings()
    assert len(ms) == 84
    assert ms[0].participants == set(['E', 'H', 'I', 'J', 'L'])
    assert ms[0].facilitators == set(['*A', '*G'])


def test_get_meetings_treating_if_need_be_as_no(csv_str):
    poll = dp.from_csv_str(csv_str)
    ms = poll.get_meetings(treat_if_need_be_as_yes=False)
    assert len(ms) == 84
    assert len(ms[0].participants) == 3 and len(ms[0].facilitators) == 1


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
        tmpfile
        ):
    spy_loader = csv_file_parameter_with_spy_loader.loader
    dispatcher.add_param(csv_file_parameter_with_spy_loader)
    dispatcher.dispatch(['--file', str(tmpfile)])
    assert hasattr(spy_loader.opened_file, 'read')


def test_loader(csv_file):
    loader = dpcl.Loader()
    loader.opened_file = open(csv_file, 'r')
    doodle_poll = loader.load()
    assert len(doodle_poll.respondents) == 13


def test_loader_get_command_line_parameters():
    loader = dpcl.Loader()
    params = loader.get_command_line_parameters()
    assert len(params) == 1
    assert isinstance(params[0], dpcl.CsvFileParameter)


def test_loader_set_opened_file(csv_file):
    opened_file = open(csv_file, 'r')
    loader = dpcl.Loader()
    loader.set_opened_file(opened_file)
    assert loader.opened_file == opened_file
