class App:
    def __init__(self):
        self.command_line_processor = None
        self.doodle_poll_loader = None
        self.meeting_generator = None
        self.meeting_filter = None
        self.statistics_reporter = None
        self.candidate_generator = None
        self.candidate_filter = None
        self.solution_reporter = None

        self.dry_run = False

    def run(self, command_line_args):
        self.process_command_line(command_line_args)
        doodle_poll = self.doodle_poll_loader.load()
        meetings = self.meeting_generator.generate(doodle_poll)
        meetings = self.meeting_filter.filter(meetings)
        self.statistics_reporter.report(self.meeting_filter)
        self.halt_if_dry_run()
        candidates = self.candidate_generator.generate(meetings)
        solutions = self.candidate_filter.filter(candidates)
        self.solution_reporter.report(solutions)

    def process_command_line(self):
        components = [
            self,
            self.command_line_processor,
            self.doodle_poll_loader,
            self.meeting_generator,
            self.meeting_filter,
            self.statistics_reporter,
            self.candidate_generator,
            self.candidate_filter,
            self.solution_reporter,
        ]
        params = self.get_all_command_line_params()
        self.command_line_processor.add_all_params(params)
        self.command_line_processor.process(self.command_line_arguments)

    def get_all_command_line_params(self):
        params = []
        for c in components:
            params.extend(c.get_command_line_params())
        return params

    def get_command_line_params(self):
        return [DryRunParameter(self)]

    def halt_if_dry_run(self):
        if self.dry_run:
            sys.exit(0)


class DryRunParameter(command_line.Parameter):
    name = '--dry-run'
    opts = {
        'help': 'something useful',
        'default': False,
        'action': 'store_true'
    }

    def __init__(self, app):
        self.app = app

    def process(self, param, arg):
        self.app.dry_run = arg
