import unittest
from datetime import datetime

# system under test
from lib import doodlepoll


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
        self.parsed_meetings = doodlepoll.parse_csv_string(DOODLEPOLL_CSV_STRING)

    def test_parse_into_a_list(self):
        self.assertTrue(isinstance(self.parsed_meetings, list))

    def test_elements_are_meetings(self):
        self.assertTrue(all(isinstance(m, doodlepoll.Meeting) for m in self.parsed_meetings))

    def test_meetings_have_a_datetime(self):
        self.assertTrue(all(isinstance(m.datetime, datetime) for m in self.parsed_meetings))

    def test_meetings_datetimes_are_joined_from_rows_3_to_5(self):
        self.assertEqual(
            self.parsed_meetings[0].datetime,
            datetime.strptime('May 2019 20 11:00 AM', '%b %Y %d %I:%M %p')
        )
        self.assertEqual(
            self.parsed_meetings[1].datetime,
            datetime.strptime('May 2019 20 12:00 PM', '%b %Y %d %I:%M %p')
        )
        self.assertEqual(
            self.parsed_meetings[4].datetime,
            datetime.strptime('May 2019 21 12:00 PM', '%b %Y %d %I:%M %p')
        )

    def test_meetings_have_names_of_those_who_can_attend(self):
        self.assertListEqual(
            self.parsed_meetings[0].those_who_can_attend,
            [
                'Facilitator 1',
                'Participant 1'
            ]
        )

    def test_meetings_have_names_of_those_who_can_attend_if_need_be(self):
        self.assertListEqual(
            self.parsed_meetings[1].those_who_can_attend_if_need_be,
            [
                'Facilitator 1',
                'Participant 1'
            ]
        )

    def test_if_need_be_is_a_subset_of_those_who_can_attend(self):
        for m in self.parsed_meetings:
            self.assertTrue(
                all(x in m.those_who_can_attend for x in m.those_who_can_attend_if_need_be)
            )
