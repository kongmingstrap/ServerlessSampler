import os
import boto3


dynamodb = boto3.resource('dynamodb')


class UsersRepository(object):
    def __init__(self):
        self._dynamodb = dynamodb

    def fetchUsers(self):
        """
        put table
        """
        try:
            table = self._dynamodb.Table(os.environ['USER_TABLE_NAME'])
            response = table.scan()
            users = response.get('Items')

            return users
        except Exception as e:
            print('Exception: {e}'.format(e))
