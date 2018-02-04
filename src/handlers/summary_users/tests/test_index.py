import index
from send_report_service import SendReportService
from summary_users_service import SummaryUsersService


class TestIndex(object):
    def test_normal(self, monkeypatch):
        """
        normal test
        """

        monkeypatch.setattr(SummaryUsersService, 'summary_report', lambda x: x)
        monkeypatch.setattr(SendReportService, 'send_report', lambda *x: x)

        index.handler({}, {})
