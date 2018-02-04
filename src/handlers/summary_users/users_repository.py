import os
import boto3


class UsersRepository(object):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def fetchUsers(self):
        """
        put table
        """

        try:
            table = self.dynamodb.Table(os.environ['USER_TABLE_NAME'])
            response = table.scan()
            users = response.get('Items')

            return users
        except Exception as e:
            print('Exception: {e}'.format(e))
