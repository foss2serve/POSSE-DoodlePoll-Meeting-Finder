import abc

import find_meetings.command_line as command_line


class Base(command_line.Parameter):
    def __init__(self):
        self.filter = None

    def set_filter(self, filter_):
        self.filter = filter_

    def process(self, parameter, argument):
        partial = self.partially_evaluate_condition(argument)
        self.meeting_filter.add_condition(partial)

    def partially_evaluate_condition(self, argument):
        partial = functools.partial(self.condition, argument)
        functools.update_wrapper(partial)

    @abc.abstractmethod
    def condition(self, threshold, meeting):
        return True


class Days(Base):
    name = '--days'
    opts = {
        'help': 'something useful',
        'default': Days.parse('0123456'),
        'type': Days.parse
    }

    @classmethod
    def parse(cls, string):
        days = tuple(int(x) for x in list(str))
        assert all(0 <= d <= 6 for d in days)
        return days

    def condition(self, arg, meeting):
        f'Day is one of {arg}'
        return meeting.weekday in arg


class MinStart(Base):
    name = '--min-start'
    opts = {
        'help': 'something useful',
        'default': 0,
        'type': int
    }

    def condition(self, threshold, meeting):
        f'Minimum start time of {threshold}'
        return meeting.start_hour_24 >= threshold


class MaxStart(Base):
    name = '--max-start'
    opts = {
        'help': 'something useful',
        'type': int
    }

    def condition(self, threshold, meeting):
        f'Maximum start time of {threshold}'
        return meeting.start_hour_24 <= threshold
