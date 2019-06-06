import sys

import pytest

import meeting_finder.doodle_poll_loader as loader
import meeting_finder.command_line as command_line


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
    loader_ = loader.DoodlePollLoader()
    loader_.opened_file = open(csv_file, 'r')
    doodle_poll = loader_.load()
    assert len(doodle_poll.respondents) == 13
