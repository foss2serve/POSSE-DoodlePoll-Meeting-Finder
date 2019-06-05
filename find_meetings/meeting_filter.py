import find_meetings.meeting_condition as condition


class MeetingFilter:
    def __init__(self):
        self.supported_conditions = [
            condition.Days(),
            condition.MinStart(),
            condition.MaxStart()
            ]

        for c in self.supported_conditions:
            c.set_filter(self)

    def get_command_line_parameters(self):
        return self.supported_conditions
