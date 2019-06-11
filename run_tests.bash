#!/usr/bin/env bash

set -e

flake8 meeting_finder
mypy --strict meeting_finder
coverage run --branch --source=meeting_finder -m pytest tests
coverage report -m
