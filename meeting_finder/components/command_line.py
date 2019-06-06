'''
command_line glues together components and commend-line arguments.
Components define command-line parameters and register a callback
to receive their arguments. These callbacks can then configure the
components appropriately. This allows all the code for handling
command-line parameters/arguments for a component to be stored
with that component.
'''

import argparse
import typing as ty

import meeting_finder.app_base as app_base
import meeting_finder.components.command_line_base as cl_base


class Dispatcher(app_base.Component):
    '''
    Components add command line parameters to a Dispatcher.
    The Dispatcher processes the command line arguments and dispatches
    to their registered parameter.
    '''

    def __init__(self) -> None:
        self.parameters: ty.List[cl_base.Parameter] = []

    def add_param(self, parameter: cl_base.Parameter) -> None:
        self.parameters.append(parameter)

    def add_all_params(
            self,
            parameters: ty.Iterable[cl_base.Parameter]
            ) -> None:
        for p in parameters:
            self.add_param(p)

    def dispatch(self, args: ty.List[str]) -> None:
        parser = argparse.ArgumentParser()
        seen: ty.Set[str] = set()
        for param in self.parameters:
            if param.name not in seen:
                seen.add(param.name)
                parser.add_argument(param.name, **param.opts)

        parsed_args = parser.parse_args(args)

        for param in self.parameters:
            name = param.name
            if name.startswith('--'):
                name = name[2:]
            name = name.replace('-', '_')
            if hasattr(parsed_args, name):
                argument = getattr(parsed_args, name)
                param.process(argument)
