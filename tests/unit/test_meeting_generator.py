from meeting_finder.meeting_generator import (
    generate_meetings_from_doodle_poll
)


def test_generate_meetings_treating_if_need_be_as_yes(doodle_poll):
    ms = generate_meetings_from_doodle_poll(
        doodle_poll, treat_if_need_be_as_yes=True)
    assert len(ms) == 84
    print(ms[0].facilitators)
    assert set([str(p) for p in ms[0].participants]) == set(['E', 'H', 'I', 'J', 'L'])
    assert set([str(p) for p in ms[0].facilitators]) == set(['*A', '*G'])


def test_generate_meetings_treating_if_need_be_as_no(doodle_poll):
    ms = generate_meetings_from_doodle_poll(
        doodle_poll, treat_if_need_be_as_yes=False)
    assert len(ms) == 84
    assert len(ms[0].participants) == 3 and len(ms[0].facilitators) == 1
