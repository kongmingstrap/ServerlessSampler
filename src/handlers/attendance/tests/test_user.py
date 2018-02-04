import pytest

from user import User


class TestUser(object):
    @pytest.mark.parametrize(
        'data, expected', [
            (
                {
                    'user_id': '0001',
                    'attendance': 'stay',
                    'place': 'FUKUOKA'
                },
                {
                    'UserId': '0001',
                    'Attendance': 'stay',
                    'Place': 'FUKUOKA'
                }
            )
        ])
    def test_normal(self, data, expected, monkeypatch):
        """
        normal test
        """

        user_data = User(
            data.get('user_id'),
            data.get('place'),
            data.get('attendance')
        )

        actual = user_data.user_data()

        assert actual == expected
