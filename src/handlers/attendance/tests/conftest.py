import os

import boto3
import pytest


def pytest_runtest_setup():
    """
    Setup Lambda function
    """

    os.environ['USER_TABLE_NAME'] = 'user_table'


@pytest.fixture(scope='session')
def dynamodb():
    """
    dynamodb fixture
    """

    return boto3.resource('dynamodb', endpoint_url='http://localhost:4569')


@pytest.fixture(scope='function')
def create_user_table(dynamodb, request):
    """
    fixture user_table
    """

    dynamodb.create_table(
        TableName=os.environ['USER_TABLE_NAME'],
        AttributeDefinitions=[
            {
                'AttributeName': 'UserId',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'UserId',
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        })

    def delete_user_table():
        dynamodb.Table(os.environ['USER_TABLE_NAME']).delete()
    request.addfinalizer(delete_user_table)
