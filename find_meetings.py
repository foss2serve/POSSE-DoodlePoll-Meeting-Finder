import argparse


def main():
    args = argparser().parse_args()
    doodlepoll_csv_string = load_file(args.doodlepoll_csv_filepath)
    meetings = parse_doodlepoll_csv_string_into_meetings(doodlepoll_csv_string)
    meetings = filter_meetings(meetings, meeting_filters(args))
    meeting_sets = generate_meeting_sets(meetings)
    meeting_sets = filter_meeting_sets(meeting_sets, args.meeting_set_filters)
    print_meeting_sets(meeting_sets)


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('doodlepoll_csv_filepath', type=str,
                    help='Location of the doodlepoll csv file.')
    parser.add_argument('--exclude-weekend', action='store_true', default=False,
                    help='Exclude weekend meetings.')
    parser.add_argument('--exclude-before', type=int, default=0,
                    help='Exclude meetings starting before hour (24 clock).')
    parser.add_argument('--exclude-after', type=int, default=24,
                    help='Exclude meetings starting after hour (24 clock).')
    parser.add_argument('--exclude-smaller-than', type=int, default=1,
                    help='Exclude meetings with fewer than the given number of participants.')
    parser.add_argument('--exclude-larger-than', type=int, default=float('inf'),
                    help='Exclude meetings with more than the given number of participants.')
    return parser


def load_file(filepath):
    with open(filepath) as f:
        return f.read()


def parse_doodlepoll_csv_string_into_meetings(csv_string):
    from lib import doodlepoll
    meetings = doodlepoll.parse_csv_string(csv_string)
    return meetings


def meeting_filters(args):
    filters = []
    if args.exclude_weekend:
        filters.append(doodlepoll.exclude_meetings_on_weekends())
    if args.exclude_before:
        filters.append(doodlepoll.exclude_meetings_starting_before(args.exclude_before))
    if args.exclude_after:
        filters.append(doodlepoll.exclude_meetings_starting_before(args.exclude_after))
    if args.exclude_smaller_than:
        filters.append(doodlepoll.exclude_meetings_with_attendees_fewer_than(args.exclude_smaller_than))
    if args.exclude_larger_than:
        filters.append(doodlepoll.exclude_meetings_with_attendees_greater_than(args.exclude_larger_than))
    return filters


def filter_meetings(meetings, meeting_filters):
    return meetings


if __name__ == '__main__':
    main()
