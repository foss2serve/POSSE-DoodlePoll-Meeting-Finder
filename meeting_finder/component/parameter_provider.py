import abc
import typing as ty

import meeting_finder.core.command_line as cl


class ParameterProvider(abc.ABC):
    @abc.abstractmethod
    def get_command_line_parameters(self) -> ty.Iterable[cl.Parameter]:
        pass
