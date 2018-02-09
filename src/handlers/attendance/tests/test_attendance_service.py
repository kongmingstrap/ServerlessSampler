import pytest

from user import User
from attendance_service import AttendanceService
from attendance_repository import AttendanceRepository


class TestAttendanceService(object):
    @pytest.mark.parametrize(
        'user', [
            (User('0001', 'FUKUOKA', 'star'))
        ])
    def test_normal(self, user, monkeypatch):
        """
        normal test
        """

        monkeypatch.setattr(AttendanceRepository, 'put_user', lambda *x: x)

        AttendanceService().send_report(user)
