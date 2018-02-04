import json
import pytest

from user_factory import UserFactory


class TestUserFactory(object):
    @pytest.mark.parametrize(
        'event', [
            ({
                'body': json.dumps({
                    'user_id': '0001',
                    'attendance': 'stay',
                    'place': 'FUKUOKA',
                })
            })
        ])
    def test_normal(self, event, monkeypatch):
        """
        normal test
        """

        UserFactory().from_event(event)
