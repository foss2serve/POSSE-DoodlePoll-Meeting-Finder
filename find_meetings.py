import argparse
from datetime import datetime
from itertools import combinations


def main():
    args = argparser().parse_args()
    doodlepoll_csv_string = load_file(args.doodlepoll_csv_filepath)
    meetings = parse_meetings(doodlepoll_csv_string)
    meetings = filter_meetings(meetings, meeting_filters(args))
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
        filters.append(min_start_filter(args.min_start))
    if args.max_start:
        filters.append(max_start_filter(args.max_start))
    if args.min_people:
        filters.append(min_people_filter(args.min_people))
    if args.max_people:
        filters.append(max_people_filter(args.max_people))
    if args.min_facilitators:
        filters.append(min_facilitator_filter(args.min_facilitators))
    if args.max_facilitators:
        filters.append(max_facilitator_filter(args.max_facilitators))
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

        those_who_can_attend = []
        for j in range(6, len(rows)-1):
            if rows[j][i]:
                those_who_can_attend.append(rows[j][0])

        those_who_can_attend_if_need_be = []
        for j in range(6, len(rows)-1):
            if rows[j][i] == '(OK)':
                those_who_can_attend_if_need_be.append(rows[j][0])

        m = Meeting(dt, those_who_can_attend, those_who_can_attend_if_need_be)
        meetings.append(m)

    return meetings


def parse_people(csv_string):
    meetings = []
    rows = csv_string.split('\n')
    rows = [r.split(',') for r in rows]
    return [rows[j][0] for j in range(6, len(rows)-1)]


class Meeting:
    def __init__(self, datetime, those_who_can_attend, those_who_can_attend_if_need_be):
        self.datetime = datetime
        self.those_who_can_attend = those_who_can_attend
        self.those_who_can_attend_if_need_be = those_who_can_attend_if_need_be

    def __str__(self):
        s = [self.datetime.strftime('%c')]
        for a in self.those_who_can_attend:
            s.append(f'{a}')
        return '\n    '.join(s)


def min_start_filter(hour):
    return lambda m: m.datetime.hour >= hour


def max_start_filter(hour):
    return lambda m: m.datetime.hour <= hour


def min_people_filter(n):
    return lambda m: len(m.those_who_can_attend) >= n


def max_people_filter(n):
    return lambda m: len(m.those_who_can_attend) <= n


def min_facilitator_filter(n):
    return lambda m: len([x for x in m.those_who_can_attend if x[0] == '*']) >= n


def max_facilitator_filter(n):
    return lambda m: len([x for x in m.those_who_can_attend if x[0] == '*']) <= n


def all_participants_covered_filter(people):
    participants = filter_participants(people)
    return lambda ms: len(participants - people_who_can_make_at_least_one_meeting_in(ms)) == 0


def filter_participants(people):
    return set(filter(lambda p: p[0] != '*', people))


def people_who_can_make_at_least_one_meeting_in(meeting_set):
    ps = set()
    for m in meeting_set:
        ps |= set(m.those_who_can_attend)
    return ps


class Filter:
    def __init__(self):
        self.name = type(self).__name__
        self.count_in = None
        self.count_out = None

    def apply_and_count(self, items):
        self.count_in = len(items)
        items = self.filter(items)
        self.count_out = len(items)
        self.filtered = self.count_in - self.count_out
        return items

    def __str__(self):
        return f'{self.name}: in={self.count_in} out={self.count_out} filtered={self.count_in-self.count_out}'


class WeekdayFilter(Filter):
    def __init__(self):
        super().__init__()

    def filter(self, meetings):
        return list(filter(weekday_filter_fn, meetings))


def weekday_filter_fn(meeting):
    return meeting.datetime.weekday() < 5




if __name__ == '__main__':
    main()
