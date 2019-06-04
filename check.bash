#!/usr/bin/env bash

set -e

flake8 find_meetings
mypy --strict find_meetings
python -m find_meetings
