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
from lib.doodlepoll import DoodlePoll


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


if __name__ == '__main__':
    main()
