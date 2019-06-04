from typing import Iterable

from find_meetings.meeting import Meeting
from find_meetings.condition import filter_items
from find_meetings.condition import get_conditions
from find_meetings import rejection_counter


def main() -> None:
    meetings: Iterable[Meeting] = [
        Meeting(0, 0, frozenset(['bob']), frozenset(['betty']))
    ]
    conditions = get_conditions({
        'Days': [0, 2, 3],
        'MinStart': 1,
    })
    conditions, counts = rejection_counter.wrap(conditions)
    meetings = filter_items(meetings, conditions)
    for name, count in counts.items():
        print(name, count)


if __name__ == '__main__':
    main()
