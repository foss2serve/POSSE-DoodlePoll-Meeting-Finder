import meeting_finder.doodle_poll as doodle_poll


def test_from_csv_str(csv_str):
    dp = doodle_poll.from_csv_str(csv_str)
    assert len(dp.respondents) == 13
    assert dp.respondents == \
        ('*A', 'B', 'C', 'D', 'E', 'F', '*G', 'H', 'I', 'J', '*K', 'L', '*M')
    assert len(dp.datetimes) == 84
    assert len(dp.availabilities) == 13
    assert len(dp.availabilities[0]) == 84


def test_get_meetings(csv_str):
    dp = doodle_poll.from_csv_str(csv_str)
    ms = dp.get_meetings()
    assert len(ms) == 84
    assert ms[0].participants == set(['E', 'H', 'I', 'J', 'L'])
    assert ms[0].facilitators == set(['*A', '*G'])


def test_get_meetings_treating_if_need_be_as_no(csv_str):
    dp = doodle_poll.from_csv_str(csv_str)
    ms = dp.get_meetings(treat_if_need_be_as_yes=False)
    assert len(ms) == 84
    assert len(ms[0].participants) == 3 and len(ms[0].facilitators) == 1
