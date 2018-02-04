import index
from fetch_report_service import FetchReportService
from post_message_service import PostMessageService


class TestIndex(object):
    def test_normal(self, monkeypatch):
        """
        normal test
        """

        monkeypatch.setattr(FetchReportService, 'fetch_report', lambda x: x)
        monkeypatch.setattr(PostMessageService, 'post_message', lambda *x: {})

        index.handler({}, {})
