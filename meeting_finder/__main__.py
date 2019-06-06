'''
This is the command-line entry point for this application.
It loads and runs the application with the command line arguments.
'''

import sys
import typing as ty

import meeting_finder.app as app


def main(args: ty.List[str]) -> None:
    app.with_default_components().run(args)


if __name__ == '__main__':
    main(sys.argv[1:])
