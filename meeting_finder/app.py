'''
The application uses components to find
sets of meetings that meet
specified conditions.
'''

import typing as ty

import meeting_finder.app_base as app_base
import meeting_finder.components.command_line as cl
import meeting_finder.components.csv_doodle_poll as cdp
import meeting_finder.components.meeting_generator as mg
# import meeting_finder.components.flow as flow
# import meeting_finder.components.candidate as can
# import meeting_finder.components.solution as sol


def with_default_components() -> 'App':
    '''Return an App with default components.'''
    return App(
        cl.Dispatcher(),
        cdp.CsvDoodlePollFileLoader(),
        mg.MeetingGenerator()
        # mtg.Filter(),
        # mtg.FilterReporter(),
        # can.SearchSpaceReporter(),
        # flow.DryRunSentinel(),
        # can.Generator(),
        # can.Filter(),
        # can.Reporter(),
        # sol.Reporter()
        )


class App:
    def __init__(
            self,
            command_line_dispatcher: cl.Dispatcher,
            csv_doodle_poll_loader: cdp.CsvDoodlePollFileLoader,
            meeting_generator: mg.MeetingGenerator
            # meeting_filter: mtg.Filter,
            # meeting_filter_reporter: mtg.FilterReporter,
            # candidate_search_space_reporter: can.SearchSpaceReporter,
            # dry_run_sentinel: flow.DryRunSentinel,
            # candidate_generator: can.Generator,
            # candidate_filter: can.Filter,
            # candidate_filter_reporter: can.Reporter,
            # solution_reporter: sol.Reporter
            ) -> None:
        self.command_line_dispatcher = command_line_dispatcher
        self.csv_doodle_poll_loader = csv_doodle_poll_loader
        self.meeting_generator = meeting_generator
        # self.meeting_filter = meeting_filter
        # self.meeting_filter_reporter = meeting_filter_reporter
        # self.candidate_search_space_reporter = \
        #     candidate_search_space_reporter
        # self.dry_run_sentinel = dry_run_sentinel
        # self.candidate_generator = candidate_generator
        # self.candidate_filter = candidate_filter
        # self.candidate_filter_reporter = candidate_filter_reporter
        # self.solution_reporter = solution_reporter

        self.gather_cl_params([
            self.csv_doodle_poll_loader,
            self.meeting_generator,
            # self.meeting_filter,
            # self.meeting_filter_reporter,
            # self.candidate_search_space_reporter,
            # self.dry_run_sentinel,
            # self.candidate_generator,
            # self.candidate_filter,
            # self.candidate_filter_reporter,
            # self.solution_reporter,
        ])

    def gather_cl_params(
            self,
            components: ty.Iterable[app_base.Component]
            ) -> None:
        for c in components:
            params = c.get_cl_params()
            self.command_line_dispatcher.add_all_params(params)

    def run(self, args: ty.List[str]) -> None:
        self.command_line_dispatcher.dispatch(args)
        poll = self.csv_doodle_poll_loader.load()
        meetings = self.meeting_generator.generate(poll)
        assert meetings is not None
        # meetings = self.meeting_filter.filter(meetings)
        # self.meeting_filter_reporter.report(self.meeting_filter)
        # self.candidate_search_space_reporter.report(meetings)
        # self.dry_run_sentinel.maybe_halt()
        # candidates = self.candidate_generator.generate(meetings)
        # solutions = self.candidate_filter.filter(candidates)
        # self.solution_reporter.report(solutions)
        # self.candidate_filter_reporter.report(self.candidate_filter)
