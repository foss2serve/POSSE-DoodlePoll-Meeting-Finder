import argparse
from datetime import datetime
from itertools import combinations, product
from collections import Counter
import operator as op
from functools import reduce
import sys


def main():
    args = get_commandline_arguments()
    path_to_csv_file = args.doodlepoll_csv_filepath
    if_need_be_yes = True
    if args.treat_if_need_be_as_no:
        print("Treating if-need-be responses as No.")
        if_need_be_yes = False
    doodle_poll = DoodlePoll.from_csv_file(path_to_csv_file, if_need_be_yes)
    meetings = doodle_poll.get_meetings()
    meetings = list(meetings)
    filters = get_meeting_filters(args)
    meetings = list(apply_filters(filters, meetings))
    print_filter_status(filters)
    calculate_and_print_number_of_candidates(len(meetings), args.k)
    halt_if(args.dry_run)
    meeting_sets = generate_meeting_sets(meetings, args.k)
    meeting_set_filters = get_meeting_set_filters(args, doodle_poll)
    meeting_sets = apply_filters(meeting_set_filters, meeting_sets)
    print_meeting_sets(meeting_sets)
    print_filter_status(meeting_set_filters)


def get_commandline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'doodlepoll_csv_filepath',
        type=str,
        help='Location of the doodlepoll csv file.')
    parser.add_argument(
        'k',
        type=int,
        help='Number of meetings in a solution.')
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Just report filter counts and the number of candidates.')
    parser.add_argument(
        '--treat-if-need-be-as-no',
        action='store_true',
        help='If set, if-need-be responses will be considered No responses.')
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
        default=2,
        help='Exclude meetings with fewer than the given number of people who can attend.')
    parser.add_argument(
        '--max-people',
        type=int,
        help='Exclude meetings with more than the given number of people who can attend.')
    parser.add_argument(
        '--min-facilitators',
        type=int,
        default=1,
        help='Exclude meetings with fewer than the given number of facilitators.')
    parser.add_argument(
        '--max-facilitators',
        type=int,
        help='Exclude meetings with more than the given number of facilitators.')
    parser.add_argument(
        '--min-participants',
        type=int,
        default=1,
        help='Exclude meetings with fewer than the given number of participants.')
    parser.add_argument(
        '--max-participants',
        type=int,
        help='Exclude meetings with more than the given number of participants.')
    parser.add_argument(
        '--max-facilitations',
        type=int,
        help='Exclude candidates where any one facilitator must facilitate more than the given number of meetings.')
    return parser.parse_args()


def get_meeting_filters(args):
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
    if args.min_participants:
        filters.append(MinParticipantsFilter(args.min_participants))
    if args.max_participants:
        filters.append(MaxParticipantsFilter(args.max_participants))
    return filters


def apply_filters(filters, items):
    for f in filters:
        items = f.apply(items)
    return items


def print_filter_status(filters):
    for f in filters:
        print(f)


def calculate_and_print_number_of_candidates(number_of_meetings, meetings_per_candidate):
    n = number_of_meetings
    k = meetings_per_candidate
    total = ncr(n, k)
    print(f'There are {total} {k}-meeting candidates')


def halt_if(c):
    if c:
        sys.exit(0)


def generate_meeting_sets(meetings, k):
    return combinations(meetings, k)


def get_meeting_set_filters(args, doodle_poll):
    filters = []
    participants = doodle_poll.get_participants()
    filters.append(AllParticipantsCanAttendAtLeastOneMeetingFilter(participants))
    if args.max_facilitations:
        filters.append(MaxFacilitationsFilter(args.min_facilitators, args.max_facilitations))
    return filters


def print_meeting_sets(meeting_sets):
    for i, ms in enumerate(meeting_sets, 1):
        print(f'========= Solution {i} =============')
        for m in ms:
            print()
            print(m)
        print()


class DoodlePoll:
    @classmethod
    def from_csv_file(cls, path_to_file, if_need_be_yes=True):
        string = load_file(path_to_file)
        return cls.from_csv_string(string, if_need_be_yes)

    @classmethod
    def from_csv_string(cls, string, if_need_be_yes=True):
        lines = string.split('\n')
        raw_data = [ln.split(',') for ln in lines]
        datetimes = tuple(cls.parse_datetimes(raw_data))
        people = tuple(cls.parse_people(raw_data))
        matrix = cls.parse_availability_matrix(raw_data, if_need_be_yes)
        return DoodlePoll(people, datetimes, matrix)

    @classmethod
    def parse_datetimes(cls, raw_data):
        # this looks like a hyphon, but it's not
        DOODLEPOLL_TIME_SEPARATOR = ' – '
        times = raw_data[3:6]
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
            yield dt

    @classmethod
    def parse_people(cls, raw_data):
        rows = raw_data[6:cls.get_index_of_count_row(raw_data)]
        for r in rows:
            name = r[0]
            if name[0] == '*':
                yield Facilitator(name)
            else:
                yield Participant(name)

    @classmethod
    def parse_availability_matrix(cls, raw_data, if_need_be_yes=True):
        rows = [row[1:] for row in raw_data[6:cls.get_index_of_count_row(raw_data)]]
        for row in rows:
            for i in range(len(row)):
                if row[i] == 'OK':
                    row[i] = Yes()
                elif row[i] == '(OK)':
                    if if_need_be_yes:
                        row[i] = IfNeedBeYes()
                    else:
                        row[i] = IfNeedBeNo()
                else:
                    row[i] = No()
        return rows

    @classmethod
    def get_index_of_count_row(cls, raw_data):
        for i in range(-1, -len(raw_data), -1):
            if raw_data[i][0] == 'Count':
                return i

    def __init__(self, people, datetimes, availability_matrix):
        self.people = people
        self.datetimes = datetimes
        self.availability_matrix = availability_matrix

    def get_meetings(self):
        for dt in self.datetimes:
            yield Meeting(dt, self.get_people_who_can_attend(dt))

    def get_people_who_can_attend(self, datetime):
        datetime_index = self.datetimes.index(datetime)
        for person_index, person_is_available in enumerate(self.availability_matrix):
            if person_is_available[datetime_index]:
                yield self.people[person_index]

    def get_participants_who_can_attend(self, datetime):
        return filter(lambda x: x.is_participant(), self.get_people_who_can_attend(datetime))

    def get_facilitators_who_can_attend(self, datetime):
        return filter(lambda x: x.is_facilitator(), self.get_people_who_can_attend(datetime))

    def get_people(self):
        return self.people

    def get_participants(self):
        return filter(lambda x: x.is_participant(), self.get_people())

    def get_facilitators(self):
        return filter(lambda x: x.is_facilitator(), self.get_people())


def load_file(filepath):
    with open(filepath) as f:
        return f.read()


class Person:
    def __init__(self, name):
        self.name = name

    def is_facilitator(self):
        return False

    def is_participant(self):
        return False

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.name)


class Facilitator(Person):
    def is_facilitator(self):
        return True


class Participant(Person):
    def is_participant(self):
        return True


class Response:
    def is_if_need_be(self):
        return False


class Yes(Response):
    def __bool__(self):
        return True


class No(Response):
    def __bool__(self):
        return False


class IfNeedBe(Response):
    def is_if_need_be(self):
        return True


class IfNeedBeYes(IfNeedBe, Yes):
    pass


class IfNeedBeNo(IfNeedBe, No):
    pass


class Meeting:
    def __init__(self, datetime, people_who_can_attend):
        self.datetime = datetime
        if people_who_can_attend is not None:
            self.people_who_can_attend = tuple(people_who_can_attend)
        else:
            self.people_who_can_attend = None

    def get_people_who_can_attend(self):
        return self.people_who_can_attend

    def get_participants_who_can_attend(self):
        return filter(lambda x: x.is_participant(), self.get_people_who_can_attend())

    def get_facilitators_who_can_attend(self):
        return filter(lambda x: x.is_facilitator(), self.get_people_who_can_attend())

    def __str__(self):
        s = [self.datetime.strftime('%c')]
        for a in self.get_people_who_can_attend():
            s.append(f'{a}')
        return '\n    '.join(s)


class Filter:
    def apply(self, items):
        self.success_count = 0
        self.fail_count = 0
        self.count_in = 0
        self.count_out = 0
        return filter(self.counting_condition, items)

    def counting_condition(self, item):
        self.count_in += 1
        if self.condition(item):
            self.success_count += 1
            self.count_out += 1
            return True
        else:
            self.fail_count += 1
            return False

    def __str__(self):
        if hasattr(self, 'name'):
            name = self.name
        else:
            name = type(self).__name__
        return f'{name}:  in={self.count_in}, filtered={self.count_in-self.count_out}, out={self.count_out}'


class WeekdayFilter(Filter):
    def condition(self, meeting):
        return meeting.datetime.weekday() < 5


class MinStartFilter(Filter):
    def __init__(self, hour):
        self.hour = hour
        self.name = f'MinStartFilter({hour})'

    def condition(self, meeting):
        return meeting.datetime.hour >= self.hour


class MaxStartFilter(Filter):
    def __init__(self, hour):
        self.hour = hour
        self.name = f'MaxStartFilter({hour})'

    def condition(self, meeting):
        return meeting.datetime.hour <= self.hour


class MinPeopleFilter(Filter):
    def __init__(self, n):
        self.n = n
        self.name = f'MinPeopleFilter({n})'

    def condition(self, meeting):
        return len(list(meeting.get_people_who_can_attend())) >= self.n


class MaxPeopleFilter(Filter):
    def __init__(self, n):
        self.n = n
        self.name = f'MaxPeopleFilter({n})'

    def condition(self, meeting):
        return len(list(meeting.get_people_who_can_attend())) <= self.n


class MinFacilitatorsFilter(Filter):
    def __init__(self, n):
        self.n = n
        self.name = f'MinFacilitatorsFilter({n})'

    def condition(self, meeting):
        return len(list(meeting.get_facilitators_who_can_attend())) >= self.n


class MaxFacilitatorsFilter(Filter):
    def __init__(self, n):
        self.n = n
        self.name = f'MaxFacilitatorsFilter({n})'

    def condition(self, meeting):
        return len(list(meeting.get_facilitators_who_can_attend())) <= self.n


class MinParticipantsFilter(Filter):
    def __init__(self, n):
        self.n = n
        self.name = f'MinParticipantsFilter({n})'

    def condition(self, meeting):
        return len(list(meeting.get_participants_who_can_attend())) >= self.n


class MaxParticipantsFilter(Filter):
    def __init__(self, n):
        self.n = n
        self.name = f'MaxParticipantsFilter({n})'

    def condition(self, meeting):
        return len(list(meeting.get_participants_who_can_attend())) <= self.n


class AllParticipantsCanAttendAtLeastOneMeetingFilter(Filter):
    def __init__(self, all_participants):
        self.all_participants = set(all_participants)

    def condition(self, meeting_set):
        coverage = set()
        for m in meeting_set:
            coverage = coverage.union(set(m.get_participants_who_can_attend()))
        return len(coverage) == len(self.all_participants)


class MaxFacilitationsFilter(Filter):
    def __init__(self, min_facilitators, max_facilitations):
        self.max_facilitations = max_facilitations
        self.min_facilitators = min_facilitators
        self.name = f'MaxFacilitationsFilter(min_facilitators={min_facilitators}, max_facilitations={max_facilitations})'

    def condition(self, meeting_set):
        each_meetings_minimum_facilitator_combinations = []
        for m in meeting_set:
            c = combinations(m.get_facilitators_who_can_attend(), self.min_facilitators)
            each_meetings_minimum_facilitator_combinations.append(c)
        for configuration in product(*each_meetings_minimum_facilitator_combinations):
            c = Counter([f for meeting_facilitators in configuration for f in meeting_facilitators])
            if all(v <= self.max_facilitations for v in c.values()):
                return True
        return False


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom


if __name__ == '__main__':
    main()
