import argparse


def main():
    args = argparser().parse_args()
    doodlepoll_csv_string = load_file(args.doodlepoll_csv_filepath)
    meetings = parse_meetings(doodlepoll_csv_string)
    meetings = filter_meetings(meetings, meeting_filters(args))
    meeting_sets = generate_meeting_sets(meetings, args.k)
    meeting_sets = filter_meeting_sets(meeting_sets, meeting_set_filters(args, parse_participants(doodlepoll_csv_string)))
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
        '--min-attendance',
        type=int,
        help='Exclude meetings with fewer than the given number of attendees.')
    parser.add_argument(
        '--max-attendance',
        type=int,
        help='Exclude meetings with more than the given number of attendees.')
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


def parse_meetings(csv_string):
    from lib import doodlepoll
    meetings = doodlepoll.parse_csv_string(csv_string)
    return meetings


def parse_participants(csv_string):
    from lib import doodlepoll
    participants = doodlepoll.parse_participants(csv_string)
    return participants


def meeting_filters(args):
    from lib import doodlepoll
    filters = []
    if args.weekday:
        filters.append(doodlepoll.weekday_filter())
    if args.min_start:
        filters.append(doodlepoll.min_start_filter(args.min_start))
    if args.max_start:
        filters.append(doodlepoll.max_start_filter(args.max_start))
    if args.min_attendance:
        filters.append(doodlepoll.min_attendance_filter(args.min_attendance))
    if args.max_attendance:
        filters.append(doodlepoll.max_attendance_filter(args.max_attendance))
    if args.min_facilitators:
        filters.append(doodlepoll.min_facilitator_filter(args.min_facilitators))
    if args.max_facilitators:
        filters.append(doodlepoll.max_facilitator_filter(args.max_facilitators))
    return filters


def filter_meetings(meetings, meeting_filters):
    print(len(meetings))
    for f in meeting_filters:
        print('Applying', f)
        meetings = list(filter(f, meetings))
        print(len(meetings))
    return meetings


def generate_meeting_sets(meetings, k):
    from itertools import combinations
    return combinations(meetings, k)


def meeting_set_filters(args, participants):
    from lib import doodlepoll
    return [doodlepoll.all_participants_covered_filter(participants)]


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


if __name__ == '__main__':
    main()
