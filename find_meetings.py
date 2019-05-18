DOODLE_POLL_CSV_FILE='Doodle.csv'
FACILITATORS = [
    'Stoney Jackson',
    'Lori Postner',
    'Greg Hislop',
    'Darci Burdge',
    'Heidi Ellis',
    'Clif Kussmaul'
]
NUMBER_OF_MEETINGS=3
FILTER_MEETINGS_WITH_FEWER_ATTENDEES_THAN=6
FILTER_MEETINGS_WITH_FEWER_FACILITATORS_THAN=2
FILTER_MEETINGS_WITH_TIME_LATER_THAN=21
FILTER_MEETINGS_WITH_TIME_EARLIER_THAN=9

from itertools import combinations
import sys

def main():
    dp = DoodlePoll.from_csv(DOODLE_POLL_CSV_FILE)
    meetings = list(dp.yieldMeetings())
    print(len(meetings), 'meetings')

    print(f'Eliminating meetings with fewer than {FILTER_MEETINGS_WITH_FEWER_ATTENDEES_THAN} attendees.')
    meetings = [m for m in meetings if m.numberWhoCanAttend() >= FILTER_MEETINGS_WITH_FEWER_ATTENDEES_THAN]
    print(len(meetings), 'meetings')

    print(f'Eliminating meetings with fewer than {FILTER_MEETINGS_WITH_FEWER_FACILITATORS_THAN} facilitators.')
    meetings = [m for m in meetings if m.numberOfFacilitators(FACILITATORS) >= FILTER_MEETINGS_WITH_FEWER_FACILITATORS_THAN]
    print(len(meetings), 'meetings')

    print(f'Eliminating meetings after {FILTER_MEETINGS_WITH_TIME_LATER_THAN}.')
    meetings = [m for m in meetings if m.startHour() < FILTER_MEETINGS_WITH_TIME_LATER_THAN]
    print(len(meetings), 'meetings')

    print(f'Eliminating meetings before {FILTER_MEETINGS_WITH_TIME_EARLIER_THAN}.')
    meetings = [m for m in meetings if m.startHour() >= FILTER_MEETINGS_WITH_TIME_EARLIER_THAN]
    print(len(meetings), 'meetings')

    solution_count = 0
    for meeting_set in combinations(meetings, NUMBER_OF_MEETINGS):
        if all_participants_can_make_at_least_one_meeting(meeting_set, dp.getNames()):
            solution_count += 1
            print_meeting_set(meeting_set)

    print(solution_count, 'solutions')


def all_participants_can_make_at_least_one_meeting(meeting_set, all_people):
    all_people = list(all_people)
    for m in meeting_set:
        for n in m.names:
            if n in all_people:
                all_people.remove(n)
    for p in all_people:
        if p not in FACILITATORS:
            return False
    return True


def print_meeting_set(meeting_set):
    print("===========================")
    for m in meeting_set:
        print(m)


def isWeekend(datetime):
    return datetime.weekday() < 5


class DoodlePoll:
    '''Results of a DoodlePoll.'''

    @classmethod
    def from_csv(cls, csv_filename):
        rows = cls.load_csv_rows(csv_filename)
        return DoodlePoll(rows)

    @classmethod
    def load_csv_rows(cls, csv_filename):
        import csv
        rows = []
        with open(csv_filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        return rows

    @classmethod
    def save_csv_rows(cls, csv_filename, rows):
        import csv
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def __init__(self, rows):
        self.rows = rows

    def removeName(self, name):
        i = 0
        while i < len(self.rows):
            if self.rows[i][0] == name:
                break
            i += 1
        self.rows = self.rows[:i] + self.rows[i+1:]

    def yieldMeetings(self):
        for datetime in self.getDatetimes():
            names = self.yieldNamesOfThoseWhoCanAttend(datetime)
            yield Meeting(datetime, names)

    def yieldNamesOfThoseWhoCanAttend(self, datetime):
        for person in self.getNames():
            if self.canAttend(person, datetime):
                yield person

    def canAttend(self, name, datetime):
        i = self.nameIndex(name)
        j = self.datetimeIndex(datetime)
        return bool(self.getValues()[i][j])

    def nameIndex(self, name):
        return self.getNames().index(name)

    def datetimeIndex(self, datetime):
        return self.getDatetimes().index(datetime)

    def getDatetimes(self):
        dts = []
        ts = self.getDateTimeSection()
        for col_i in range(1, len(ts[0])):
            if ts[0][col_i] != '':
                month_year = ts[0][col_i]
            if ts[1][col_i] != '':
                date = ts[1][col_i]
            if ts[2][col_i] != '':
                time = ts[2][col_i]
            dts.append(f'{month_year} {date} {time}')
        return dts

    def getNames(self):
        return [r[0] for r in self.getDataSection()]

    def getValues(self):
        data = self.getDataSection()
        values = [r[1:] for r in data]
        return values

    def getDateTimeSection(self):
        return self.rows[3:6]

    def getDataSection(self):
        return self.rows[6:-1]


class Meeting:
    def __init__(self, datetime, names):
        self.datetime = datetime
        self.names = list(names)

    def __str__(self):
        return '\n'.join([self.datetime] + ['  ' + n for n in self.names])

    def numberWhoCanAttend(self):
        return len(self.names)

    def getDatetime(self):
        import re
        from datetime import datetime
        dt_str = self.datetime
        ## The dash in the expression below is not a normal dash.
        ## Be careful not to delete it and press -.
        p = re.compile(r'Mon |Tue |Wed |Thu |Fri |Sat |Sun | – .*')
        dt_str = p.sub('', dt_str)
        dt = datetime.strptime(dt_str, '%B %Y %d %I:%M %p')
        return dt

    def numberOfFacilitators(self, facilitators):
        count = 0
        for f in facilitators:
            if f in self.names:
                count += 1
        return count

    def startHour(self):
        return self.getDatetime().hour


if __name__ == '__main__':
    main()
