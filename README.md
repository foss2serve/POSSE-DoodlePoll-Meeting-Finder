
## Development

### Install development environment

1. Install Git
2. Fork this project on GitHub
3. Clone your fork
4. Install Python 3.6 or higher
5. Install pipenv
6. On non-MacOS platforms, delete `Pipfile.lock`
7. Install all python-based project dependencies, including those needed for development

```
$ pipenv install --dev
```

### Running the development environment

```
$ pipenv shell
```

### Exiting the development environment

```
$ exit
```

### Run run tests

First run the development environment, and then,

```
$ ./run_tests.bash
```
