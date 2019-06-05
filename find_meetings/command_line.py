class Dispatcher:
    def __init__(self):
        self.parameters = []

    def add_param(self, parameter):
        self.parameters.append(parameter)

    def add_all_params(self, parameters):
        for p in parameters:
            self.add_param(p)

    def dispatch(self, args):
        parser = argparse.ArgumentParser()
        for param, optional in self.parameters:
            parser.add_argument(param.name, **param.opts)

        parsed_args = parser.parser_args(args)

        for parameter in self.parameters:
            if hasattr(parsed_args, param):
                argument = parsed_args[param]
                parameter.process(param, argument)


class Parameter(abc.ABC):
    @abc.abstractmethod
    def process(self, parameter, argument):
        pass
