import os
import boto3


dynamodb = boto3.resource('dynamodb')


class AttendanceRepository(object):
    def __init__(self):
        self._dynamodb = dynamodb

    def put_user(self, data):
        """
        put table
        """
        try:
            table = self._dynamodb.Table(os.environ['USER_TABLE_NAME'])
            table.put_item(Item=data.user_data())
        except Exception as e:
            print('Exception: {e}'.format(e))
