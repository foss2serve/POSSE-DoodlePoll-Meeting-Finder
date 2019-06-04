import find_meetings.doodle_poll as doodle_poll


csv_str = '''"Poll ""IRC 2""",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
https://doodle.com/poll/ywrnff8rb33uewnr,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,May 2019,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,Mon 20,,,,,,,,,,,,,,Tue 21,,,,,,,,,,,,,,Wed 22,,,,,,,,,,,,,,Thu 23,,,,,,,,,,,,,,Fri 24,,,,,,,,,,,,,,Sat 25,,,,,,,,,,,,,
,7:00 AM – 8:00 AM,8:00 AM – 9:00 AM,9:00 AM – 10:00 AM,10:00 AM – 11:00 AM,11:00 AM – 12:00 PM,12:00 PM – 1:00 PM,1:00 PM – 2:00 PM,2:00 PM – 3:00 PM,3:00 PM – 4:00 PM,4:00 PM – 5:00 PM,5:00 PM – 6:00 PM,6:00 PM – 7:00 PM,7:00 PM – 8:00 PM,8:00 PM – 9:00 PM,7:00 AM – 8:00 AM,8:00 AM – 9:00 AM,9:00 AM – 10:00 AM,10:00 AM – 11:00 AM,11:00 AM – 12:00 PM,12:00 PM – 1:00 PM,1:00 PM – 2:00 PM,2:00 PM – 3:00 PM,3:00 PM – 4:00 PM,4:00 PM – 5:00 PM,5:00 PM – 6:00 PM,6:00 PM – 7:00 PM,7:00 PM – 8:00 PM,8:00 PM – 9:00 PM,7:00 AM – 8:00 AM,8:00 AM – 9:00 AM,9:00 AM – 10:00 AM,10:00 AM – 11:00 AM,11:00 AM – 12:00 PM,12:00 PM – 1:00 PM,1:00 PM – 2:00 PM,2:00 PM – 3:00 PM,3:00 PM – 4:00 PM,4:00 PM – 5:00 PM,5:00 PM – 6:00 PM,6:00 PM – 7:00 PM,7:00 PM – 8:00 PM,8:00 PM – 9:00 PM,7:00 AM – 8:00 AM,8:00 AM – 9:00 AM,9:00 AM – 10:00 AM,10:00 AM – 11:00 AM,11:00 AM – 12:00 PM,12:00 PM – 1:00 PM,1:00 PM – 2:00 PM,2:00 PM – 3:00 PM,3:00 PM – 4:00 PM,4:00 PM – 5:00 PM,5:00 PM – 6:00 PM,6:00 PM – 7:00 PM,7:00 PM – 8:00 PM,8:00 PM – 9:00 PM,7:00 AM – 8:00 AM,8:00 AM – 9:00 AM,9:00 AM – 10:00 AM,10:00 AM – 11:00 AM,11:00 AM – 12:00 PM,12:00 PM – 1:00 PM,1:00 PM – 2:00 PM,2:00 PM – 3:00 PM,3:00 PM – 4:00 PM,4:00 PM – 5:00 PM,5:00 PM – 6:00 PM,6:00 PM – 7:00 PM,7:00 PM – 8:00 PM,8:00 PM – 9:00 PM,7:00 AM – 8:00 AM,8:00 AM – 9:00 AM,9:00 AM – 10:00 AM,10:00 AM – 11:00 AM,11:00 AM – 12:00 PM,12:00 PM – 1:00 PM,1:00 PM – 2:00 PM,2:00 PM – 3:00 PM,3:00 PM – 4:00 PM,4:00 PM – 5:00 PM,5:00 PM – 6:00 PM,6:00 PM – 7:00 PM,7:00 PM – 8:00 PM,8:00 PM – 9:00 PM
*A,OK,,,,,OK,OK,OK,OK,OK,,,,,,,OK,OK,OK,OK,,,,OK,,,,,,,OK,OK,OK,OK,OK,OK,OK,,,,,,,,OK,OK,OK,OK,OK,OK,OK,OK,,,,,,,OK,OK,OK,OK,OK,OK,OK,,,,,,,,(OK),(OK),(OK),(OK),(OK),(OK),(OK),(OK),,,,
B,,OK,OK,OK,OK,OK,OK,OK,OK,OK,OK,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,OK,OK,OK,OK,OK,OK,OK,OK,OK,OK,,,,,,,,,,,,,,,,,
C,,,,,,,,,,,OK,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,OK,,,,,,,,,,,,,,,OK,,,,,,,,,,,,,,,,,,,,
D,,,,OK,OK,OK,OK,OK,,,,,,,,,,,,,,,,,,,,,,,,OK,OK,OK,OK,OK,OK,OK,,,,,,,,OK,OK,OK,OK,OK,OK,,,,,,,,,OK,OK,OK,OK,,,,,,,,,,,,,,,,,,,,,
E,OK,OK,OK,OK,OK,OK,,,,,,,OK,OK,,,,,,OK,OK,OK,OK,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,OK,OK,OK,,,,OK,OK,OK,OK,,,,,,,,,,,,,,,,,
F,,,,,,OK,OK,OK,OK,OK,OK,OK,OK,OK,,,,,,OK,OK,OK,OK,OK,OK,OK,OK,OK,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,OK,OK,OK,OK,OK,OK,OK,OK,OK
*G,(OK),,,,,,OK,OK,,,,,,,,,,,,,,,,,,,,,,,,OK,OK,OK,OK,OK,,,,,,,,,,OK,OK,OK,OK,OK,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
H,(OK),,,,,,,OK,,,OK,OK,,,(OK),OK,,,OK,OK,OK,OK,,,,,,,(OK),OK,OK,OK,OK,,,OK,OK,OK,OK,OK,,,,,,,OK,OK,OK,OK,OK,OK,,,,,(OK),OK,OK,OK,OK,OK,OK,,,,,,,,,,,,,,,,,,,,,
I,(OK),,OK,OK,,,,,OK,OK,OK,,,,,,,,,,,OK,,,,,,,,OK,OK,,,,,,,OK,OK,,,,,,,,,OK,(OK),,,,OK,OK,,,,OK,OK,,,,,,OK,OK,OK,OK,OK,OK,,,,,,,,OK,OK,OK,OK,OK,OK,OK
J,OK,,,,(OK),OK,,,,(OK),,,,,,,,,(OK),OK,,,,,OK,,OK,,,,,,(OK),OK,,,,(OK),,,,(OK),,,,,(OK),OK,,OK,,,,,,OK,,,,,(OK),OK,,,,(OK),,,OK,OK,,,,,,OK,OK,OK,OK,(OK),(OK),(OK),(OK),OK
*K,,,,,,,,,,,,,,,(OK),OK,OK,OK,OK,OK,OK,OK,OK,OK,OK,OK,(OK),(OK),(OK),OK,OK,OK,OK,OK,OK,OK,OK,OK,OK,OK,(OK),(OK),,,,OK,OK,OK,OK,OK,OK,OK,OK,OK,(OK),(OK),OK,OK,,,,,,,,(OK),(OK),(OK),(OK),(OK),,,,,,,,,,,,,,
L,OK,(OK),(OK),(OK),(OK),(OK),(OK),(OK),,,,,,,(OK),(OK),(OK),(OK),(OK),(OK),(OK),(OK),,,,,,,OK,OK,OK,OK,OK,OK,OK,OK,,,,,,,OK,OK,OK,OK,OK,OK,OK,OK,,,,,,,,,,,,,,,,,,,,,OK,OK,OK,OK,OK,OK,OK,OK,,,,,,
*M,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,OK,OK,OK,OK,OK,OK,OK,OK,OK,OK,OK,OK,,,OK,,,OK,OK,OK,OK,OK,,,,,,,,,,,,,,,,,,,
Count,0:3:11,2:1:11,3:1:10,4:1:9,3:2:9,6:1:7,5:1:8,6:1:7,4:0:10,4:1:9,5:0:9,2:0:12,2:0:12,2:0:12,0:3:11,2:1:11,2:1:11,2:1:11,3:2:9,6:1:7,4:1:9,5:1:8,3:0:11,3:0:11,3:0:11,2:0:12,2:1:11,1:1:12,1:2:11,4:0:10,5:0:9,6:0:8,6:1:7,6:0:8,5:0:9,6:0:8,4:0:10,4:1:9,3:0:11,2:0:12,0:1:13,0:2:12,1:0:13,2:0:12,3:0:11,6:0:8,7:1:6,9:0:5,8:1:5,8:0:6,5:0:9,4:0:10,3:0:11,3:0:11,1:1:12,1:1:12,1:1:12,6:0:8,5:0:9,5:0:9,5:1:8,6:0:8,5:0:9,5:0:9,5:0:9,3:2:9,3:1:10,1:1:12,2:1:11,2:1:11,1:0:13,1:0:13,1:1:12,1:1:12,1:1:12,4:1:9,4:1:9,5:1:8,4:1:9,3:2:9,3:1:10,3:1:10,3:1:10,4:0:10'''


def test_from_csv_str():
    dp = doodle_poll.from_csv_str(csv_str)
    assert len(dp.respondents) == 13
    assert dp.respondents == \
        ('*A', 'B', 'C', 'D', 'E', 'F', '*G', 'H', 'I', 'J', '*K', 'L', '*M')
    assert len(dp.datetimes) == 84
    assert len(dp.availabilities) == 13
    assert len(dp.availabilities[0]) == 84


def test_get_meetings():
    dp = doodle_poll.from_csv_str(csv_str)
    ms = dp.get_meetings()
    assert len(ms) == 84
    assert ms[0].participants == set(['E', 'H', 'I', 'J', 'L'])
    assert ms[0].facilitators == set(['*A', '*G'])


def test_get_meetings_treating_if_need_be_as_no():
    dp = doodle_poll.from_csv_str(csv_str)
    ms = dp.get_meetings(treat_if_need_be_as_yes=False)
    assert len(ms) == 84
    assert len(ms[0].participants) == 3 and len(ms[0].facilitators) == 1
