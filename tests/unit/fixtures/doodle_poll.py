import pytest

from meeting_finder.csv_doodle_poll import parse_doodle_poll_from_csv_str


@pytest.fixture
def doodle_poll(csv_str):
    return parse_doodle_poll_from_csv_str(csv_str)
