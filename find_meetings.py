import argparse
from datetime import datetime
from itertools import combinations
import operator as op
from functools import reduce


def main():
    args = argparser().parse_args()
    doodlepoll_csv_string = load_file(args.doodlepoll_csv_filepath)
    meetings = parse_meetings(doodlepoll_csv_string)
    meetings = filter_meetings(meetings, meeting_filters(args))
    if args.dry_run:
        print(ncr(len(meetings), args.k), 'candidates')
    else:
        meeting_sets = generate_meeting_sets(meetings, args.k)
        meeting_sets = filter_meeting_sets(meeting_sets, meeting_set_filters(args, parse_people(doodlepoll_csv_string)))
        print_meeting_sets(meeting_sets)


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'doodlepoll_csv_filepath',
        type=str,
        help='Location of the doodlepoll csv file.')
    parser.add_argument(
        'k',
        type=int,
        help='Number of meetings in a solution.'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Just report filter counts and the number of candidates.'
    )
    parser.add_argument(
        '--weekday',
        action='store_true',
        help='Exclude weekend meetings.')
    parser.add_argument(
        '--min-start',
        type=int,
        help='Exclude meetings starting before hour (24 clock).')
    parser.add_argument(
        '--max-start',
        type=int,
        help='Exclude meetings starting after hour (24 clock).')
    parser.add_argument(
        '--min-people',
        type=int,
        help='Exclude meetings with fewer than the given number of people who can attend.')
    parser.add_argument(
        '--max-people',
        type=int,
        help='Exclude meetings with more than the given number of people who can attend.')
    parser.add_argument(
        '--min-facilitators',
        type=int,
        help='Exclude meetings with fewer than the given number of facilitators.')
    parser.add_argument(
        '--max-facilitators',
        type=int,
        help='Exclude meetings with more than the given number of facilitators.')
    return parser


def load_file(filepath):
    with open(filepath) as f:
        return f.read()


def meeting_filters(args):
    filters = []
    if args.weekday:
        filters.append(WeekdayFilter())
    if args.min_start:
        filters.append(MinStartFilter(args.min_start))
    if args.max_start:
        filters.append(MaxStartFilter(args.max_start))
    if args.min_people:
        filters.append(MinPeopleFilter(args.min_people))
    if args.max_people:
        filters.append(MaxPeopleFilter(args.max_people))
    if args.min_facilitators:
        filters.append(MinFacilitatorsFilter(args.min_facilitators))
    if args.max_facilitators:
        filters.append(MaxFacilitatorsFilter(args.max_facilitators))
    return filters


def filter_meetings(meetings, meeting_filters):
    print(len(meetings))
    for f in meeting_filters:
        if isinstance(f, Filter):
            meetings = f.apply_and_count(meetings)
            print(f)
        else:
            print('Applying', f)
            meetings = list(filter(f, meetings))
            print(len(meetings))
    return meetings


def generate_meeting_sets(meetings, k):
    return combinations(meetings, k)


def meeting_set_filters(args, people):
    return [all_participants_covered_filter(people)]


def filter_meeting_sets(meeting_sets, meeting_set_filters):
    meeting_sets = list(meeting_sets)
    for f in meeting_set_filters:
        meeting_sets = list(filter(f, meeting_sets))
    return meeting_sets


def print_meeting_sets(meeting_sets):
    meeting_sets = list(meeting_sets)
    for i, ms in enumerate(meeting_sets, 1):
        print(f'========= Solution {i} =============')
        for m in ms:
            print()
            print(m)
        print()


 # this looks like a hyphon, but it's not
DOODLEPOLL_TIME_SEPARATOR = ' – '


def parse_meetings(s):
    meetings = []
    rows = s.split('\n')
    rows = [r.split(',') for r in rows]
    times = rows[3:6]
    for i in range(1, len(times[0])):
        if times[0][i]:
            month_year = times[0][i]
        if times[1][i]:
            day_date = times[1][i]
            date = day_date.split(' ')[1]
        if times[2][i]:
            time = times[2][i]
            start_time = time.split(DOODLEPOLL_TIME_SEPARATOR)[0]
        dt = datetime.strptime(f'{month_year} {date} {start_time}', '%b %Y %d %I:%M %p')

        people_who_can_attend = []
        for j in range(6, len(rows)-1):
            if rows[j][i]:
                people_who_can_attend.append(rows[j][0])

        people_who_can_attend_if_need_be = []
        for j in range(6, len(rows)-1):
            if rows[j][i] == '(OK)':
                people_who_can_attend_if_need_be.append(rows[j][0])

        m = Meeting(dt, people_who_can_attend, people_who_can_attend_if_need_be)
        meetings.append(m)

    return meetings


def parse_people(csv_string):
    meetings = []
    rows = csv_string.split('\n')
    rows = [r.split(',') for r in rows]
    return [rows[j][0] for j in range(6, len(rows)-1)]


class Meeting:
    def __init__(self, datetime, people_who_can_attend, people_who_can_attend_if_need_be):
        self.datetime = datetime
        self.people_who_can_attend = people_who_can_attend
        if self.people_who_can_attend is not None:
            self.facilitators_who_can_attend = [x for x in self.people_who_can_attend if x[0] == '*']
        else:
            self.facilitators_who_can_attend = None
        self.people_who_can_attend_if_need_be = people_who_can_attend_if_need_be

    def __str__(self):
        s = [self.datetime.strftime('%c')]
        for a in self.people_who_can_attend:
            s.append(f'{a}')
        return '\n    '.join(s)


def all_participants_covered_filter(people):
    participants = filter_participants(people)
    return lambda ms: len(participants - people_who_can_make_at_least_one_meeting_in(ms)) == 0


def filter_participants(people):
    return set(filter(lambda p: p[0] != '*', people))


def people_who_can_make_at_least_one_meeting_in(meeting_set):
    ps = set()
    for m in meeting_set:
        ps |= set(m.people_who_can_attend)
    return ps


class Filter:
    def apply_and_count(self, items):
        self.count_in = len(items)
        items = list(filter(self.condition, items))
        self.count_out = len(items)
        self.filtered = self.count_in - self.count_out
        return items

    def __str__(self):
        if hasattr(self, 'name'):
            name = self.name
        else:
            name = type(self).__name__
        return f'{name}: in={self.count_in} out={self.count_out} filtered={self.count_in-self.count_out}'


class WeekdayFilter(Filter):
    def condition(self, meeting):
        return meeting.datetime.weekday() < 5


class MinStartFilter(Filter):
    def __init__(self, hour):
        self.hour = hour

    def condition(self, meeting):
        return meeting.datetime.hour >= self.hour


class MaxStartFilter(Filter):
    def __init__(self, hour):
        self.hour = hour

    def condition(self, meeting):
        return meeting.datetime.hour <= self.hour


class MinPeopleFilter(Filter):
    def __init__(self, n):
        self.n = n

    def condition(self, meeting):
        return len(meeting.people_who_can_attend) >= self.n


class MaxPeopleFilter(Filter):
    def __init__(self, n):
        self.n = n

    def condition(self, meeting):
        return len(meeting.people_who_can_attend) <= self.n


class MinFacilitatorsFilter(Filter):
    def __init__(self, n):
        self.n = n

    def condition(self, meeting):
        return len(meeting.facilitators_who_can_attend) >= self.n


class MaxFacilitatorsFilter(Filter):
    def __init__(self, n):
        self.n = n

    def condition(self, meeting):
        return len(meeting.facilitators_who_can_attend) <= self.n


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom


if __name__ == '__main__':
    main()
