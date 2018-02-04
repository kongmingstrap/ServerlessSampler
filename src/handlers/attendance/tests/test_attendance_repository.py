import pytest

from attendance_repository import AttendanceRepository


class TestAttendanceRepository(object):
    @pytest.mark.usefixtures('create_user_table')
    @pytest.mark.parametrize(
        'data', [
            ({
                'UserId': '0001'
            })
        ])
    def test_normal(self, data, dynamodb, monkeypatch):
        """
        normal test
        """

        repository = AttendanceRepository()
        repository.dynamodb = dynamodb
        repository.put_user(data)
