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

    def test_min_start_filter(self):
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
        filter = find_meetings.MinStartFilter(6)
        meetings = filter.apply_and_count(meetings)
        self.assertListEqual(meetings, [six, seven])

    def test_max_start_filter(self):
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
        filter = find_meetings.MaxStartFilter(6)
        meetings = filter.apply_and_count(meetings)
        self.assertListEqual(meetings, [four, five, six])

    def test_min_people_filter(self):
        meetings = [
            Meeting(None, [], []),
            Meeting(None, ['1'], ['1']),
            Meeting(None, ['1', '2'], ['1', '2']),
            Meeting(None, ['1', '2', '3'], ['1', '2', '3']),
        ]
        zero = meetings[0]
        one = meetings[1]
        two = meetings[2]
        three = meetings[3]
        filter = find_meetings.MinPeopleFilter(2)
        meetings = filter.apply_and_count(meetings)
        self.assertListEqual(meetings, [two, three])

    def test_max_people_filter(self):
        meetings = [
            Meeting(None, [], []),
            Meeting(None, ['1'], ['1']),
            Meeting(None, ['1', '2'], ['1', '2']),
            Meeting(None, ['1', '2', '3'], ['1', '2', '3']),
        ]
        zero = meetings[0]
        one = meetings[1]
        two = meetings[2]
        three = meetings[3]
        filter = find_meetings.MaxPeopleFilter(2)
        meetings = filter.apply_and_count(meetings)
        self.assertListEqual(meetings, [zero, one, two])


    def test_min_facilitators_filter(self):
        meetings = [
            Meeting(None, [], []),
            Meeting(None, ['1'], ['1']),
            Meeting(None, ['1', '*2'], ['1', '*2']),
            Meeting(None, ['1', '*2', '*3'], ['1', '*2', '*3']),
        ]
        zero_a = meetings[0]
        zero_b = meetings[1]
        one = meetings[2]
        two = meetings[3]
        filter = find_meetings.MinFacilitatorsFilter(1)
        meetings = filter.apply_and_count(meetings)
        self.assertListEqual(meetings, [one, two])


    def test_max_facilitators_filter(self):
        meetings = [
            Meeting(None, [], []),
            Meeting(None, ['1'], ['1']),
            Meeting(None, ['1', '*2'], ['1', '*2']),
            Meeting(None, ['1', '*2', '*3'], ['1', '*2', '*3']),
        ]
        zero_a = meetings[0]
        zero_b = meetings[1]
        one = meetings[2]
        two = meetings[3]
        filter = find_meetings.MaxFacilitatorsFilter(1)
        meetings = filter.apply_and_count(meetings)
        self.assertListEqual(meetings, [zero_a, zero_b, one])
