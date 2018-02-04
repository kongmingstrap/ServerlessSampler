import pytest

from send_report_service import SendReportService
from put_report_repository import PutReportRepository


class TestAttendanceService(object):
    @pytest.mark.parametrize(
        'report', [
            ({'UserId': '0001'}),
            ({}),
            (None)
        ])
    def test_normal(self, report, monkeypatch):
        """
        normal test
        """

        monkeypatch.setattr(PutReportRepository, 'put_report', lambda *x: x)

        SendReportService().send_report(report)
