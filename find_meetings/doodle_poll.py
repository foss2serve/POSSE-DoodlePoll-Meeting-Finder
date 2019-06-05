'''Responsible for parsing and internalizing DoodlePoll results into a
data structure (DoodlePoll) that can then produce a list of Meetings.'''

import datetime
import enum
from typing import Iterable
from typing import List

import find_meetings.meetings as meetings


class Response(enum.Enum):
    NO = 0
    YES = 1
    IF_NEED_BE = 2


class DoodlePoll:
    def __init__(
            self,
            respondents: Iterable[str],
            datetimes: Iterable[datetime.datetime],
            availabilities: Iterable[Iterable[Response]]
            ) -> None:
        self.respondents = tuple(respondents)
        self.datetimes = tuple(datetimes)
        self.availabilities = tuple(tuple(r) for r in availabilities)

    def get_meetings(
            self,
            treat_if_need_be_as_yes: bool = True
            ) -> Iterable[meetings.Meeting]:
        ms = []
        for col, dt in enumerate(self.datetimes):
            facilitators: List[str] = []
            participants: List[str] = []
            for row, name in enumerate(self.respondents):
                r = self.availabilities[row][col]
                if r is Response.YES \
                    or (treat_if_need_be_as_yes
                        and r is Response.IF_NEED_BE):
                    if name[0] == '*':
                        facilitators.append(name)
                    else:
                        participants.append(name)
            m = meetings.Meeting(dt, facilitators, participants)
            ms.append(m)
        return ms


def from_csv_str(csv_str: str) -> DoodlePoll:
    data = [line.split(',') for line in csv_str.split('\n')]

    for i in range(2, len(data)):
        if data[i][0] != '':
            names_start_row = i
            break
    for i in range(len(data)-1, -1, -1):
        if data[i][0] == 'Count':
            names_end_row = i
            break
    names = [r[0] for r in data[names_start_row:names_end_row]]

    start_datetimes = []
    month_year_row = names_start_row - 3
    day_date_row = names_start_row - 2
    start_stop_row = names_start_row - 1
    for i in range(1, len(data[month_year_row])):
        if data[month_year_row][i] != '':
            month_year = data[month_year_row][i]
        if data[day_date_row][i] != '':
            day_date = data[day_date_row][i]
        start_stop = data[start_stop_row][i]
        start = start_stop.split(' – ')[0]
        start_datetime_str = ' '.join([month_year, day_date, start])
        start_datetime = datetime.datetime.strptime(
            start_datetime_str, '%b %Y %a %d %I:%M %p')
        start_datetimes.append(start_datetime)

    m = [r[1:] for r in data[names_start_row:names_end_row]]
    m2: List[List[Response]] = []
    for r in m:
        row: List[Response] = []
        for v in r:
            if v == 'OK':
                row.append(Response.YES)
            elif v == '(OK)':
                row.append(Response.IF_NEED_BE)
            else:
                row.append(Response.NO)
        m2.append(row)

    return DoodlePoll(names, start_datetimes, m2)
