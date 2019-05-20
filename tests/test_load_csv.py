import unittest
import os
import tempfile
import find_meetings


class TestLoadCsv(unittest.TestCase):

    def test_load_csv(self):
        path = self.create_file_with_contents("""one,two,three\nfour,five\nsix""")
        data = find_meetings.load_csv(path)
        self.assertListEqual(
            data,
            [
                ['one', 'two', 'three'],
                ['four', 'five'],
                ['six']
            ]
        )

    def setUp(self):
        self.temp_paths = []

    def tearDown(self):
        for p in self.temp_paths:
            os.unlink(p)

    def create_file_with_contents(self, contents):
        fd, path = tempfile.mkstemp()
        with open(path, 'w') as f:
            f.write(contents)
        os.close(fd)
        return path


if __name__ == '__main__':
    unittest.main()
