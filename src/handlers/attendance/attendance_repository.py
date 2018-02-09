import os

import boto3


class AttendanceRepository(object):
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def put_user(self, data):
        """
        put table
        """

        table = self.dynamodb.Table(os.environ['USER_TABLE_NAME'])

        try:
            table.put_item(Item=data)
        except Exception as e:
            print(f'Exception: {e}')
