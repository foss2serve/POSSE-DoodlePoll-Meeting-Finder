import typing as ty

import meeting_finder.data.doodle_poll as dp
import meeting_finder.data.meeting as mtg


def generate_meetings_from_doodle_poll(
        poll: dp.DoodlePoll,
        treat_if_need_be_as_yes: bool
        ) -> ty.Iterable[mtg.Meeting]:
    ms = []
    for col, dt in enumerate(poll.datetimes):
        facilitators: ty.List[str] = []
        participants: ty.List[str] = []
        for row, name in enumerate(poll.respondents):
            r = poll.availabilities[row][col]
            if r is dp.Response.YES \
                or (treat_if_need_be_as_yes
                    and r is dp.Response.IF_NEED_BE):
                if name[0] == '*':
                    facilitators.append(name)
                else:
                    participants.append(name)
        m = mtg.Meeting(dt, facilitators, participants)
        ms.append(m)
    return ms
