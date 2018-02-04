from users_repository import UsersRepository


class SummaryUsersService(object):
    def summary_report(self):
        """
        send user data
        :param user:
        :return:
        """

        users = UsersRepository().fetchUsers()

        return users
