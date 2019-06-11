import pytest


@pytest.fixture
def csv_file(csv_str, tmpdir):
    csv_file = tmpdir.join("file.csv")
    csv_file.write(csv_str)
    return csv_file
