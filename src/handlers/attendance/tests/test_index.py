import pytest

import index
from user_factory import UserFactory
from attendance_service import AttendanceService


class TestIndex(object):
    @pytest.mark.parametrize(
        'event', [
            ({'httpMethod': 'PUT'}),
            ({'httpMethod': 'GET'}),
            ({'httpMethod': 'POST'}),
            ({'httpMethod': 'DELETE'})
        ])
    def test_normal(self, event,  monkeypatch):
        """
        normal test
        """

        monkeypatch.setattr(UserFactory, 'from_event', lambda *x: x)
        monkeypatch.setattr(AttendanceService, 'send_report', lambda *x: x)

        actual = index.handler(event, {})

        assert actual == {}
