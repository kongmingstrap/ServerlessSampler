import pytest

from summary_users_service import SummaryUsersService
from users_repository import UsersRepository


class TestIntex(object):
    @pytest.mark.parametrize(
        'users', [
            ([{'UserId': '0001'}, {'UserId': '0002'}]),
            ([]),
            (None)
        ])
    def test_normal(self, users, monkeypatch):
        """
        normal test
        """

        monkeypatch.setattr(UsersRepository, 'fetchUsers', lambda x: users)

        actual = SummaryUsersService().summary_report()

        assert actual == users
