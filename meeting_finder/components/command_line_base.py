'''
Base types that command_line depends on.
Breaks a circular dependency between app and command_line.
'''

import abc
import typing as ty


class Parameter(abc.ABC):
    '''
    Parameter provides a specification of a command line parameter
    (a la argparse) and receives a call back to its process() method
    when an argument has been passed for this parameter. This allows
    the parameter to do things like configure a particular component
    based on the argument it receives.
    '''

    name = ''
    opts: ty.Dict[str, ty.Any] = {}

    @abc.abstractmethod
    def process(self, argument: ty.Any) -> None:
        pass


class ParameterProvider(abc.ABC):
    '''A ParameterProvider provides a list of Parameters.'''
    @abc.abstractmethod
    def get_cl_params(self) -> ty.Iterable[Parameter]:
        pass
