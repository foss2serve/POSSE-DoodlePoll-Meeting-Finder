import typing as ty

import meeting_finder.app_base as app
import meeting_finder.data.doodle_poll as dp
import meeting_finder.data.meeting as mtg
import meeting_finder.functions.generate_meetings_from_doodle_poll as gm


class MeetingGenerator(app.Component):
    def __init__(self) -> None:
        self.treat_if_need_be_as_yes = True

    '''Generates meetings from a DoodlePoll.'''
    def generate(self, poll: dp.DoodlePoll) -> ty.Iterable[mtg.Meeting]:
        return gm.generate_meetings_from_doodle_poll(
            poll, self.treat_if_need_be_as_yes)
