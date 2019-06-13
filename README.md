
## Development

### Getting started

1. Install Git
2. Fork this project on GitHub
3. Clone your fork
4. Install Python 3.6 or higher
5. Install pipenv
6. On non-MacOS platforms, delete `Pipfile.lock`
7. Install all python-based project dependencies, including those needed for development
        $ pipenv install --dev

### A typical day at the office

1. Start the virtual environment
        $ pipenv shell
2. Run the tests
        $ ./run_tests.bash
3. Make, test, and commit changes until I've had enough
4. Exit the virtual environment
        $ exit
