import abc
import argparse
import typing as ty


class Dispatcher:
    def __init__(self) -> None:
        self.parameters: ty.List[Parameter] = []

    def add_param(self, parameter: 'Parameter') -> None:
        self.parameters.append(parameter)

    def add_all_params(self, parameters: ty.Iterable['Parameter']) -> None:
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


class Parameter(abc.ABC):
    name = ''
    opts: ty.Dict[str, ty.Any] = {}

    @abc.abstractmethod
    def process(self, argument: ty.Any) -> None:
        pass
