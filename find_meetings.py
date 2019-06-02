import argparse
from datetime import datetime
from itertools import combinations, product
from collections import Counter
import operator as op
from functools import reduce
import sys
import abc


def main():
    System.default_configuration().run()


class System:
    @classmethod
    def default_configuration(cls):
        system = System(argparse.ArgumentParser())
        system.install_components(get_default_component_list())
        system.process_command_line_argument_list(sys.argv[1:])
        return system

    def __init__(self, command_line_parser):
        self.command_line_parser = command_line_parser
        self.command_line_parameter_map = {}
        self.doodle_poll = None
        self.meetings_per_solution = 1
        self.meeting_list = None
        self.number_of_candidates = None
        self.is_dry_run = False
        self.meeting_filter_list = []
        self.candidate_filter_list = []
        self.minimum_number_of_facilitators = 1

    def install_components(self, components):
        for comp in components:
            comp.install_into_system(self)

    def add_command_line_parameter(self, command_line_parameter):
        self.command_line_parameter_map[name] = command_line_parameter
        (name, kwargs) = command_line_parameter.get_commaind_line_paraemter_config()
        self.command_line_parser.add_argument(name, **kwargs)

    def process_command_line_argument_list(self, command_line_argument_list):
        args = self.command_line_parser.parse_args(command_line_argument_list)
        for key in args.keys():
            self.command_line_parameter_map[key].process_command_line_argument(args[key])

    def set_doodle_poll(self, doodle_poll):
        self.doodle_poll = doodle_poll

    def set_meetings_per_solution(self, value):
        self.meetings_per_solution = value

    def run(self):
        self.get_and_filter_meetings_from_doodle_poll()
        self.print_meeting_filter_statistics()
        self.calculate_number_of_candidates()
        self.print_number_of_candidates()
        self.halt_if_this_is_a_dry_run()
        self.find_and_print_solutions()

    def get_and_filter_meetings_from_doodle_poll(self):
        meetings = self.get_meetings_from_doodle_poll(self.treat_if_need_be_as_no)
        meetings = self.filter_meetings(meetings)
        self.set_meeting_list(list(meetings))

    def get_meetings_from_doodle_poll(self, treat_if_need_be_as_no):
        return self.doodle_poll.get_meetings(treat_if_need_be_as_no)

    def filter_meetings(self, meetings):
        return self.apply_filters(self.meeting_filter_list, meetings)

    def apply_filters(filters, items):
        for f in filters:
            items = f.apply(items)
        return items

    def print_meeting_filter_statistics(self):
        for f in self.get_meeting_filter_list():
            print(f)

    def calculate_number_of_candidates(self):
        self.number_of_candidates = ncr(len(self.meeting_list), self.meetings_per_solution)

    def print_number_of_candidates(self):
        print('Number of candidates:', self.number_of_candidates)

    def halt_if_this_is_a_dry_run(self):
        if self.is_dry_run:
            sys.exit(0)

    def find_and_print_solutions(self):
        candidates = self.generate_candidates(self.meeting_list)
        solutions = self.filter_candidates(candidates)
        for sol in solutions:
            self.print_solution(sol)

    def generate_candidates(self, meeting_list):
        return combinations(meeting_list, self.meetings_per_solution)

    def filter_candidates(self, candidates):
        return self.apply_filters(self.candidate_filter_list, candidates)

    def print_solution(self, solution):
        print(solution)


def get_default_component_list():
    return [
        DoodlePollCsvFileLoader(),
        MeetingsPerSolution(),
        WeekdayOnly(),
        MinStart(),
        MaxStart(),
        MinPeople(),
        MaxPeople(),
        MinFacilitators(),
        MaxFacilitators(),
        MinParticipants(),
        MaxParticipants(),
        MaxFacilitations(),
        ]


class Component:
    __metaclass__ = abc.ABCMeta

    def install(self, system):
        self.system = system
        self.install_into_system(system)

    @abc.abstractmethod
    def install_into_system(self):
        pass


class CommandLineParameter(Component):
    __metaclass__ = abc.ABCMeta

    def install_into_system(self):
        self.system.add_command_line_parameter(self)

    @abc.abstractmethod
    def get_commaind_line_paraemter_config(self):
        '''
        Return a tuple whose first element is passed to argsparse.add_argument.
        The first element is the name or option.
        The second element is a dictionary of keyword arguments ot add_argument.
        For example ('--size', {'type':int, 'deafult':1})
        '''
        pass

    @abc.abstractmethod
    def process_command_line_argument(self, argument):
        '''Called when a command line argument is passed for this parameter.'''
        pass


class FilterParameter(CommandLineParameter):
    __metaclass__ = abc.ABCMeta

    def process_command_line_argument(self, arg):
        self.system.add_meeting_filter(self.WeekdayOnlyFilter())

    @abc.abstractmethod
    def get_filter(self):
        return None


class Filter:
    __metaclass__ = abc.ABCMeta

    def apply(self, items):
        self.success_count = 0
        self.fail_count = 0
        return filter(self.counting_condition, items)

    def counting_condition(self, item):
        if self.condition(item):
            self.success_count += 1
            return True
        else:
            self.fail_count += 1
            return False

    @abc.abstractmethod
    def condition(self, item):
        pass

    def __str__(self):
        if hasattr(self, 'name'):
            name = self.name
        else:
            name = type(self).__name__
        return f'{name}:  in={self.count_in}, filtered={self.count_in-self.count_out}, out={self.count_out}'


class ParameterizedFilter:
    __metaclass__ = abc.ABCMeta

    def __init__(self, arg):
        self.arg = arg
        self.name = f'{type(self).__name__}(arg)'


class DoodlePollCsvFileLoader(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            'csv-file',
            {
                'type': argparse.FileType('r'),
                'help': 'Path to the CSV file containing the results of a DoodlePoll.'
            }
        )

    def process_command_line_argument(self, open_file):
        string = open_file.read()
        open_file.close()
        doodle_poll = DoodlePoll.from_csv_string(string)
        self.system.set_doodle_poll(doodle_poll)


class MeetingsPerSolution(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--meetings-per-solution',
            {
                'type': int,
                'default': 1,
                'help': 'Number of meetings per solution.'
            }
        )

    def process_command_line_argument(self, arg):
        self.system.set_meetings_per_solution(arg)

class WeekdayOnly(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--weekday-only',
            {
                'action': 'store_true',
                'help': 'Only consider weekday meetings.'
            }
        )

    def get_filter(self, arg):
        return self.WeekdayOnlyFilter()

    class WeekdayOnlyFilter(Filter):
        def condition(self, meeting):
            return meeting.datetime.weekday() < 5

class MinStart(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--min-start',
            {
                'type': int,
                'default': 0,
                'help': 'Exclude meetings starting before hour (24 clock).'
            }
        )

    def get_filter(self, arg):
        return self.MinStartFilter(arg)

    class MinStartFilter(ParameterizedFilter):
        def condition(self, meeting):
            return meeting.datetime.hour >= self.arg


class MaxStart(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--max-start',
            {
                'type': int,
                'default': 23,
                'help': 'Exclude meetings starting after given hour (24 clock).'
            }
        )

    def get_filter(self, arg):
        return self.MaxStartFilter(arg)

    class MaxStartFilter(ParameterizedFilter):
        def condition(self, meeting):
            return meeting.datetime.hour <= self.arg


class MinPeople(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--min-people',
            {
                'type': int,
                'default': 2,
                'help': 'Exclude meetings with fewer than given number of people who can attend.'
            }
        )

    def get_filter(self, arg):
        return self.MinPeopleFilter(arg)

    class MinPeopleFilter(ParameterizedFilter):
        def condition(self, meeting):
            return meeting.get_number_of_people_who_can_attend() >= self.arg


class MaxPeople(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--max-people',
            {
                'type': int,
                'help': 'Exclude meetings with more than given number of people who can attend.'
            }
        )

    def get_filter(self, arg):
        return self.MaxPeopleFilter(arg)

    class MaxPeopleFilter(ParameterizedFilter):
        def condition(self, meeting):
            return meeting.get_number_of_people_who_can_attend() <= self.arg


class MinParticipants(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--min-participants',
            {
                'type': int,
                'default': 1,
                'help': 'Exclude meetings with fewer than given number of participants who can attend.'
            }
        )

    def get_filter(self, arg):
        return self.MinParticipantsFilter(arg)

    class MinParticipantsFilter(ParameterizedFilter):
        def condition(self, meeting):
            return meeting.get_number_of_participants_who_can_attend() >= self.arg


class MaxParticipants(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--max-participants',
            {
                'type': int,
                'help': 'Exclude meetings with more than given number of participants who can attend.'
            }
        )

    def get_filter(self, arg):
        return self.MaxParticipantsFilter(arg)

    class MaxParticipantsFilter(ParameterizedFilter):
        def condition(self, meeting):
            return meeting.get_number_of_participants_who_can_attend() <= self.arg


class MinFacilitators(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--min-facilitators',
            {
                'type': int,
                'default': 1,
                'help': 'Exclude meetings with fewer than given number of facilitators who can attend.'
            }
        )

    def get_filter(self, arg):
        return self.MinFacilitatorsFilter(arg)

    class MinFacilitatorsFilter(ParameterizedFilter):
        def condition(self, meeting):
            return meeting.get_number_of_facilitators_who_can_attend() >= self.arg


class MaxFacilitators(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--max-facilitators',
            {
                'type': int,
                'help': 'Exclude meetings with more than given number of facilitators who can attend.'
            }
        )

    def get_filter(self, arg):
        return self.MaxFacilitatorsFilter(arg)

    class MaxFacilitatorsFilter(ParameterizedFilter):
        def condition(self, meeting):
            return meeting.get_number_of_facilitators_who_can_attend() <= self.arg


class MaxFacilitations(CommandLineParameter):
    def get_commaind_line_config(self):
        return (
            '--max-facilitations',
            {
                'type': int,
                'help': 'Exclude candidates where any one facilitator must facilitate more than the given number of meetings.'
            }
        )

    def get_filter(self, arg):
        return self.MaxFacilitationsFilter(arg, self.system.minimum_number_of_facilitators)

    class MaxFacilitationsFilter(Filter):
        def __init__(self, arg, minimum_number_of_facilitators):
            self.arg = arg
            self.minimum_number_of_facilitators = minimum_number_of_facilitators
        def condition(self, candidate):
            each_meetings_minimum_facilitator_combinations = []
            for m in candidate:
                c = combinations(m.get_facilitators_who_can_attend(), self.minimum_number_of_facilitators)
                each_meetings_minimum_facilitator_combinations.append(c)
            for configuration in product(*each_meetings_minimum_facilitator_combinations):
                c = Counter([f for meeting_facilitators in configuration for f in meeting_facilitators])
                if all(v <= self.arg for v in c.values()):
                    return True
            return False


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
    calculate_and_print_number_of_candidates(len(meetings), args.meetings_per_solution)
    halt_if(args.dry_run)
    meeting_sets = generate_meeting_sets(meetings, args.meetings_per_solution)
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
        '--meetings-per-solution',
        type=int,
        default=1,
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
