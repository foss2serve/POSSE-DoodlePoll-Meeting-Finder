'''
Base types that app depends on.
Breaks a circular dependency between app and command_line.
'''

import typing as ty

import meeting_finder.components.command_line_base as clb


class Component(clb.ParameterProvider):
    def get_cl_params(self) -> ty.Iterable[clb.Parameter]:
        return []
