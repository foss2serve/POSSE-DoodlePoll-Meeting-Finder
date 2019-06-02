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
        meetings = [Meeting(datetime.strptime(m, '%m/%d/%Y'), None) for m in meetings]
        sat = meetings[-2]
        sun = meetings[-1]
        filter = find_meetings.WeekdayFilter()
        meetings = list(filter.apply(meetings))
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
        meetings = [Meeting(datetime.strptime(m, '%H'), None) for m in meetings]
        four = meetings[0]
        five = meetings[1]
        six = meetings[2]
        seven = meetings[3]
        filter = find_meetings.MinStartFilter(6)
        meetings = list(filter.apply(meetings))
        self.assertListEqual(meetings, [six, seven])

    def test_max_start_filter(self):
        meetings = [
            '4',
            '5',
            '6',
            '7'
        ]
        meetings = [Meeting(datetime.strptime(m, '%H'), None) for m in meetings]
        four = meetings[0]
        five = meetings[1]
        six = meetings[2]
        seven = meetings[3]
        filter = find_meetings.MaxStartFilter(6)
        meetings = list(filter.apply(meetings))
        self.assertListEqual(meetings, [four, five, six])

    def test_min_people_filter(self):
        meetings = [
            Meeting(None, []),
            Meeting(None, [find_meetings.Participant('1')]),
            Meeting(None, [find_meetings.Participant('1'), find_meetings.Facilitator('2')]),
            Meeting(None, [find_meetings.Participant('1'), find_meetings.Facilitator('2'), find_meetings.Facilitator('3')]),
        ]
        zero = meetings[0]
        one = meetings[1]
        two = meetings[2]
        three = meetings[3]
        filter = find_meetings.MinPeopleFilter(2)
        meetings = list(filter.apply(meetings))
        self.assertListEqual(meetings, [two, three])

    def test_max_people_filter(self):
        meetings = [
            Meeting(None, []),
            Meeting(None, [find_meetings.Participant('1')]),
            Meeting(None, [find_meetings.Participant('1'), find_meetings.Facilitator('2')]),
            Meeting(None, [find_meetings.Participant('1'), find_meetings.Facilitator('2'), find_meetings.Facilitator('3')]),
        ]
        zero = meetings[0]
        one = meetings[1]
        two = meetings[2]
        three = meetings[3]
        filter = find_meetings.MaxPeopleFilter(2)
        meetings = list(filter.apply(meetings))
        self.assertListEqual(meetings, [zero, one, two])


    def test_min_facilitators_filter(self):
        meetings = [
            Meeting(None, []),
            Meeting(None, [find_meetings.Participant('1')]),
            Meeting(None, [find_meetings.Participant('1'), find_meetings.Facilitator('2')]),
            Meeting(None, [find_meetings.Participant('1'), find_meetings.Facilitator('2'), find_meetings.Facilitator('3')]),
        ]
        zero_a = meetings[0]
        zero_b = meetings[1]
        one = meetings[2]
        two = meetings[3]
        filter = find_meetings.MinFacilitatorsFilter(1)
        meetings = list(filter.apply(meetings))
        self.assertListEqual(meetings, [one, two])


    def test_max_facilitators_filter(self):
        meetings = [
            Meeting(None, []),
            Meeting(None, [find_meetings.Participant('1')]),
            Meeting(None, [find_meetings.Participant('1'), find_meetings.Facilitator('2')]),
            Meeting(None, [find_meetings.Participant('1'), find_meetings.Facilitator('2'), find_meetings.Facilitator('3')]),
        ]
        zero_a = meetings[0]
        zero_b = meetings[1]
        one = meetings[2]
        two = meetings[3]
        filter = find_meetings.MaxFacilitatorsFilter(1)
        meetings = list(filter.apply(meetings))
        self.assertListEqual(meetings, [zero_a, zero_b, one])


    def test_min_participants_filter(self):
        meetings = [
            Meeting(None, []),
            Meeting(None, [find_meetings.Facilitator('*1')]),
            Meeting(None, [find_meetings.Facilitator('*1'), find_meetings.Participant('2')]),
            Meeting(None, [find_meetings.Facilitator('*1'), find_meetings.Participant('2'), find_meetings.Participant('3')]),
        ]
        zero_a = meetings[0]
        zero_b = meetings[1]
        one = meetings[2]
        two = meetings[3]
        filter = find_meetings.MinParticipantsFilter(1)
        meetings = list(filter.apply(meetings))
        self.assertListEqual(meetings, [one, two])


    def test_max_participants_filter(self):
        meetings = [
            Meeting(None, []),
            Meeting(None, [find_meetings.Facilitator('*1')]),
            Meeting(None, [find_meetings.Facilitator('*1'), find_meetings.Participant('2')]),
            Meeting(None, [find_meetings.Facilitator('*1'), find_meetings.Participant('2'), find_meetings.Participant('3')]),
        ]
        zero_a = meetings[0]
        zero_b = meetings[1]
        one = meetings[2]
        two = meetings[3]
        filter = find_meetings.MaxParticipantsFilter(1)
        meetings = list(filter.apply(meetings))
        self.assertListEqual(meetings, [zero_a, zero_b, one])
