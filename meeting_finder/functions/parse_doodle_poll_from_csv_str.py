import datetime
import typing as ty

import meeting_finder.data.doodle_poll as dp


def parse_doodle_poll_from_csv_str(csv_str: str) -> dp.DoodlePoll:
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
    m2: ty.List[ty.List[dp.Response]] = []
    for r in m:
        row: ty.List[dp.Response] = []
        for v in r:
            if v == 'OK':
                row.append(dp.Response.YES)
            elif v == '(OK)':
                row.append(dp.Response.IF_NEED_BE)
            else:
                row.append(dp.Response.NO)
        m2.append(row)

    return dp.DoodlePoll(names, start_datetimes, m2)
