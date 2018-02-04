import pytest

from fetch_report_service import FetchReportService
from fetch_report_repository import FetchReportRepository


class TestFetchReportService(object):
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

        monkeypatch.setattr(
            FetchReportRepository, 'fetch_report', lambda x: report)

        actual = FetchReportService().fetch_report()

        assert actual == report
