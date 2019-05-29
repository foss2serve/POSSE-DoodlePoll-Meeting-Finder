import unittest
from datetime import datetime
import find_meetings
from find_meetings import Meeting

class TestFilters(unittest.TestCase):
    def test_filter_weekend(self):
        meetings = [
            '5/20/2019', # Mon
            '5/21/2019',
            '5/22/2019',
            '5/23/2019',
            '5/24/2019',
            '5/25/2019',
            '5/26/2019',
        ]
        meetings = [Meeting(datetime.strptime(m, '%m/%d/%Y'), None, None) for m in meetings]
        sat = meetings[-2]
        sun = meetings[-1]
        filter = find_meetings.WeekdayFilter()
        meetings = filter.apply_and_count(meetings)
        self.assertTrue(sat not in meetings)
        self.assertTrue(sun not in meetings)
        self.assertEqual(len(meetings), 5)

    def test_filter_before(self):
        meetings = [
            '4',
            '5',
            '6',
            '7'
        ]
        meetings = [Meeting(datetime.strptime(m, '%H'), None, None) for m in meetings]
        four = meetings[0]
        five = meetings[1]
        six = meetings[2]
        seven = meetings[3]
        meetings = list(filter(find_meetings.min_start_filter(6), meetings))
        self.assertListEqual(meetings, [six, seven])

    def test_filter_after(self):
        meetings = [
            '4',
            '5',
            '6',
            '7'
        ]
        meetings = [Meeting(datetime.strptime(m, '%H'), None, None) for m in meetings]
        four = meetings[0]
        five = meetings[1]
        six = meetings[2]
        seven = meetings[3]
        meetings = list(filter(find_meetings.max_start_filter(6), meetings))
        self.assertListEqual(meetings, [four, five, six])

    def test_filter_people_fewer(self):
        meetings = [
            Meeting(None, [], []),
            Meeting(None, [1], [1]),
            Meeting(None, [1, 2], [1, 2]),
            Meeting(None, [1, 2, 3], [1, 2, 3]),
        ]
        zero = meetings[0]
        one = meetings[1]
        two = meetings[2]
        three = meetings[3]
        meetings = list(filter(find_meetings.min_people_filter(2), meetings))
        self.assertListEqual(meetings, [two, three])

    def test_filter_people_greater(self):
        meetings = [
            Meeting(None, [], []),
            Meeting(None, [1], [1]),
            Meeting(None, [1, 2], [1, 2]),
            Meeting(None, [1, 2, 3], [1, 2, 3]),
        ]
        zero = meetings[0]
        one = meetings[1]
        two = meetings[2]
        three = meetings[3]
        meetings = list(filter(find_meetings.max_people_filter(2), meetings))
        self.assertListEqual(meetings, [zero, one, two])
