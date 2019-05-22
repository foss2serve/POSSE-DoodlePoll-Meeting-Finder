# POSSE IRC Meeting Finder

Finds a sets of meetings such that each participant in a Doodle Poll can attend
at least one.

## Requirements

* Python 3.6+

## Using

1. Download Excel file from Doodle Poll.
2. Use Excel to convert it to a CSV file.
3. Edit CSV and prefix facilitators' names with * .
4. Then to print all 3-meeting solutions, from the root of the project...

```bash
$ python3 find_meetings.py path/to/Doodle.csv 3
```

## Getting help

```bash
$ python3 find_meetings.py --help
```

## Testing

In the root of the project...

```bash
$ python3 -m unittest discover
```
