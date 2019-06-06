import meeting_finder.core.meeting as meeting_


def test_from_dicts():
    ms = [
        {
            'start': 'May 2019 Mon 20 7:00 AM',
            'participants': [],
            'facilitators': []
        },
        {
            'start': 'May 2019 Mon 20 2:00 PM',
            'participants': [],
            'facilitators': []
        }
    ]
    ms = list(meeting_.from_dicts(ms))
    assert len(ms) == 2
    m = ms[0]
    assert m.start_hour_24 == 7
    assert m.weekday == 0


def test_from_tuples():
    ms = [
        ('May 2019 Mon 20 12:00 AM', [], []),
        ('May 2019 Tue 21 1:00 AM', [], []),
        ('May 2019 Wed 22 2:00 PM', [], [])
    ]
    ms = list(meeting_.from_tuples(ms))
    assert len(ms) == 3
    assert ms[0].weekday == 0


def test_filter_meetings_by_start_time():
    import operator
    ms = meeting_.from_tuples([
        ('May 2019 Mon 20 12:00 AM', [], []),
        ('May 2019 Tue 21 1:00 AM', [], []),
        ('May 2019 Wed 22 2:00 PM', [], [])
    ])
    ms = list(meeting_.filter_meetings(ms, 'start_hour_24', operator.ge, 1))
    assert len(ms) == 2


def test_filter_meetings_by_weekday():
    import operator
    ms = meeting_.from_tuples([
        ('May 2019 Mon 20 12:00 AM', [], []),
        ('May 2019 Tue 21 1:00 AM', [], []),
        ('May 2019 Wed 22 2:00 PM', [], [])
    ])
    ms = list(
        meeting_.filter_meetings(ms, 'weekday', operator.contains, (0, 2)))
    assert len(ms) == 2
