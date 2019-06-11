import meeting_finder.functions.generate_meetings_from_doodle_poll as gm


def test_generate_meetings_treating_if_need_be_as_yes(doodle_poll):
    ms = gm.generate_meetings_from_doodle_poll(
        doodle_poll, treat_if_need_be_as_yes=True)
    assert len(ms) == 84
    assert ms[0].participants == set(['E', 'H', 'I', 'J', 'L'])
    assert ms[0].facilitators == set(['*A', '*G'])


def test_generate_meetings_treating_if_need_be_as_no(doodle_poll):
    ms = gm.generate_meetings_from_doodle_poll(
        doodle_poll, treat_if_need_be_as_yes=False)
    assert len(ms) == 84
    assert len(ms[0].participants) == 3 and len(ms[0].facilitators) == 1
