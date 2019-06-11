import pytest

import meeting_finder.functions.parse_doodle_poll_from_csv_str as parser


@pytest.fixture
def doodle_poll(csv_str):
    return parser.parse_doodle_poll_from_csv_str(csv_str)
