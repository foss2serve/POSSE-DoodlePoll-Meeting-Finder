import typing as ty

import meeting_finder.app_base as app
import meeting_finder.core.doodle_poll as dp
import meeting_finder.core.meeting as mtg


class MeetingGenerator(app.Component):
    '''Generates meetings from a DoodlePoll.'''
    def generate(self, poll: dp.DoodlePoll) -> ty.Iterable[mtg.Meeting]:
        return []
