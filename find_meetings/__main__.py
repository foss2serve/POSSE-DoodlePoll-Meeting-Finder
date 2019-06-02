from system import System
from cli import CommandLineInterface


def main():
    components = [
        CommandLineInterface(),
    ]
    System(components).run()


if __name__ == '__main__':
    main()
