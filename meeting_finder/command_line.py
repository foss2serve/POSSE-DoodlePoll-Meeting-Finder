from abc import (
    ABC,
    abstractmethod
)
import argparse
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Set
)


class CommandLineParameterProvider(ABC):
    @abstractmethod
    def get_command_line_parameters(
            self
            ) -> Iterable['CommandLineParameter']:
        return []


class CommandLineParameter(CommandLineParameterProvider):
    @abstractmethod
    def get_command_line_parameter_dest(self) -> str:
        return ''

    @abstractmethod
    def get_command_line_name_or_flags(self) -> Iterable[str]:
        return ['']

    @abstractmethod
    def get_command_line_options(self) -> Dict[str, Any]:
        return {
            'help': '',
            'type': str,
            'default': '',
            'action': None,
        }

    @abstractmethod
    def process_command_line_argument(self, argument: Any) -> None:
        pass

    def get_command_line_parameters(
            self
            ) -> Iterable['CommandLineParameter']:
        return [self]


class CompositeCommandLineParameterProvider(CommandLineParameterProvider):
    def __init__(self) -> None:
        self.command_line_parameter_providers: \
            List[CommandLineParameterProvider] = []

    def add_command_line_parameter_provider(
            self, provider: CommandLineParameterProvider) -> None:
        self.command_line_parameter_providers.append(provider)

    def add_all_command_line_parameter_providers(
            self, providers: List[CommandLineParameterProvider]) -> None:
        for p in providers:
            self.add_command_line_parameter_provider(p)

    def get_command_line_parameters(self) -> Iterable[CommandLineParameter]:
        params: List[CommandLineParameter] = []
        for p in self.command_line_parameter_providers:
            params.extend(p.get_command_line_parameters())
        return params


class CommandLineProcessor(CompositeCommandLineParameterProvider):
    def process_command_line_arguments(self, args: List[str]) -> None:
        parser = argparse.ArgumentParser()
        seen: Set[str] = set()

        params = list(self.get_command_line_parameters())

        for param in params:
            dest = param.get_command_line_parameter_dest()
            flags = list(param.get_command_line_name_or_flags())
            opts = param.get_command_line_options()
            if all(n not in seen for n in flags + [dest]):
                for n in flags + [dest]:
                    seen.add(n)
                opts['dest'] = dest
                parser.add_argument(*flags, **opts)

        parsed_args = parser.parse_args(args)

        for param in params:
            name = param.get_command_line_parameter_dest()
            if hasattr(parsed_args, name):
                argument = getattr(parsed_args, name)
                param.process_command_line_argument(argument)
