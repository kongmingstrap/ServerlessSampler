import pytest

from users_repository import UsersRepository


class TestUsersRepository(object):
    @pytest.mark.usefixtures('create_user_table', 'put_user_items')
    def test_normal(self, dynamodb, monkeypatch):
        """
        normal test
        """

        repository = UsersRepository()
        repository.dynamodb = dynamodb

        actual = repository.fetchUsers()

        assert actual[0].get('UserId') == '0002'
        assert actual[1].get('UserId') == '0001'
