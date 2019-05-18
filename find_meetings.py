from itertools import combinations
import sys


from lib.doodlepoll import DoodlePoll


facilitators = [
    'Stoney Jackson',
    'Lori Postner',
    'Greg Hislop',
    'Darci Burdge',
    'Heidi Ellis',
    'Clif Kussmaul'
]


def main():
    dp = DoodlePoll.from_csv('sample_data/Doodle.csv')
    meetings = list(dp.yieldMeetings())
    print(len(meetings), 'meetings')

    print('Eliminating meetings with fewer than 6 attendees.')
    meetings = [m for m in meetings if m.numberWhoCanAttend() >= 6]
    print(len(meetings), 'meetings')

    print('Eliminating meetings with fewer than 2 facilitators.')
    meetings = [m for m in meetings if hasAtLeastTwoFacilitators(m.names)]
    print(len(meetings), 'meetings')

    print('Eliminating meetings after 5 PM.')
    meetings = [m for m in meetings if isBefore5PM(m.getDatetime())]
    print(len(meetings), 'meetings')

    print('Eliminating meetings after 9 AM.')
    meetings = [m for m in meetings if isAfter9AM(m.getDatetime())]
    print(len(meetings), 'meetings')

    print('Eliminating weekend meetings.')
    meetings = [m for m in meetings if isWeekend(m.getDatetime())]
    print(len(meetings), 'meetings')

    solution_count = 0
    for meeting_set in combinations(meetings, 3):
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
        if p not in facilitators:
            return False
    return True


def print_meeting_set(meeting_set):
    print("===========================")
    for m in meeting_set:
        print(m)


def hasAtLeastTwoFacilitators(names):
    count = 0
    for f in facilitators:
        if f in names:
            count += 1
        if count >= 2:
            return True
    return False


def isBefore5PM(datetime):
    return datetime.hour < 17


def isAfter9AM(datetime):
    return datetime.hour >= 9


def isWeekend(datetime):
    return datetime.weekday() < 5


if __name__ == '__main__':
    main()
