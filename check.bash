#!/usr/bin/env bash

set -e

flake8 find_meetings
mypy --strict find_meetings
coverage run --branch --source=find_meetings -m pytest tests
coverage report -m
