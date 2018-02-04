import pytest

from post_message_service import PostMessageService


class TestPostMessageService(object):
    @pytest.mark.parametrize(
        'report', [
            ({
                'UserId': '0001'
            })
        ])
    def test_normal(self, report, monkeypatch):
        """
        normal test
        """

        PostMessageService().post_message(report)
