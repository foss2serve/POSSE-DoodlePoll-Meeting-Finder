import pytest

from meeting_finder.command_line import (
    CommandLineParameter,
    CommandLineProcessor
)


class TestParameter(CommandLineParameter):
    def get_command_line_parameter_dest(self):
        return 'hi'

    def get_command_line_name_or_flags(self):
        return ['--hi']

    def get_command_line_options(self):
        return {
            'help': 'testing TestParameter',
            'default': 1,
            'type': int
        }

    def process_command_line_argument(self, argument):
        self.received = argument


@pytest.fixture
def parameter():
    return TestParameter()


@pytest.fixture
def command_line_processor():
    return CommandLineProcessor()


def test_dispatcher_empty(command_line_processor):
    command_line_processor.process_command_line_arguments([])
    assert command_line_processor.get_command_line_parameters() == []


def test_dispatcher_to_one_with_arg(command_line_processor, parameter):
    command_line_processor.add_command_line_parameter_provider(parameter)
    command_line_processor.process_command_line_arguments(['--hi', '2'])
    assert parameter.received == 2


def test_dispatcher_to_one_with_default(command_line_processor, parameter):
    command_line_processor.add_command_line_parameter_provider(parameter)
    command_line_processor.process_command_line_arguments([])
    assert parameter.received == 1


def test_dispatcher_to_two(command_line_processor):
    t1 = TestParameter()
    t2 = TestParameter()
    command_line_processor.add_command_line_parameter_provider(t1)
    command_line_processor.add_command_line_parameter_provider(t2)
    command_line_processor.process_command_line_arguments([])
    assert t1.received == 1
    assert t2.received == 1
