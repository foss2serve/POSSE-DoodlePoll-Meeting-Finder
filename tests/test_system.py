def test_configure():
    system = System()
    args = {
        'csvFile': tempfile.TemporaryFile(),
        'meetingsPerSolution': 6,
        'days': '2,3,4',
        'minStart': 3,
        'maxStart': 15,
        'minPeople': 4,
        # leaving out 'maxPeople'
        'maxParticipant': 5,
        'maxFacilitator': 2,
        }
    system.configure(args)
