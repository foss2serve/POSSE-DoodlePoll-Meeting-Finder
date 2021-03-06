import unittest
from datetime import datetime
import types

# system under test
import find_meetings


DOODLEPOLL_CSV_STRING = '''"Poll ""IRC 2""",,,,,,
https://doodle.com/poll/uniqueID,,,,,,
,,,,,,
,May 2019,,,,,
,Mon 20,,,Tue 21,,
,11:00 AM – 12:00 PM,12:00 PM – 1:00 PM,1:00 PM – 2:00 PM,11:00 AM – 12:00 PM,12:00 PM – 1:00 PM,1:00 PM – 2:00 PM
Facilitator 1,OK,(OK),,,,
Participant 1,OK,(OK),,OK,,
Participant 2,,OK,,,,OK
Facilitator 2,,,,OK,,
Facilitator 3,,,,OK,,
Participant 3,,,OK,OK,,
Count,the,counts,can,be,reproduced,placeholder'''


class TestParsing(unittest.TestCase):
    def setUp(self):
        self.doodle_poll = find_meetings.DoodlePoll.from_csv_string(DOODLEPOLL_CSV_STRING)
        self.parsed_meetings = self.doodle_poll.get_meetings()

    def test_parse_into_a_generator(self):
        self.assertTrue(isinstance(self.parsed_meetings, types.GeneratorType))

    def test_elements_are_meetings(self):
        self.assertTrue(all(isinstance(m, find_meetings.Meeting) for m in self.parsed_meetings))

    def test_meetings_have_a_datetime(self):
        self.assertTrue(all(isinstance(m.datetime, datetime) for m in self.parsed_meetings))

    def test_meetings_datetimes_are_joined_from_rows_3_to_5(self):
        meetings = list(self.parsed_meetings)
        self.assertEqual(
            meetings[0].datetime,
            datetime.strptime('May 2019 20 11:00 AM', '%b %Y %d %I:%M %p')
        )
        self.assertEqual(
            meetings[1].datetime,
            datetime.strptime('May 2019 20 12:00 PM', '%b %Y %d %I:%M %p')
        )
        self.assertEqual(
            meetings[4].datetime,
            datetime.strptime('May 2019 21 12:00 PM', '%b %Y %d %I:%M %p')
        )

    def test_meetings_have_names_of_people_who_can_attend(self):
        self.assertListEqual(
            list(list(self.parsed_meetings)[0].get_people_who_can_attend()),
            [
                find_meetings.Participant('Facilitator 1'),
                find_meetings.Participant('Participant 1')
            ]
        )
