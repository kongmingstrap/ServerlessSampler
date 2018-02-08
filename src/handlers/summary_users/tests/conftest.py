import os
from pathlib import Path

import boto3
import pytest


def pytest_runtest_setup():
    """
    Setup Lambda function
    """

    os.environ['USER_TABLE_NAME'] = 'user_table'
    os.environ['ATTENDANCE_DATA_BUCKET_NAME'] = 'attendance-data'


@pytest.fixture(scope='session')
def dynamodb():
    """
    dynamodb fixture
    """

    return boto3.resource('dynamodb', endpoint_url='http://localhost:4569')


@pytest.fixture(scope='session')
def s3():
    """
    s3 fixture
    """

    return boto3.resource('s3', endpoint_url='http://localhost:4572')


@pytest.fixture(scope='session')
def s3_client():
    """
    s3 client fixture
    """

    return boto3.client('s3', endpoint_url='http://localhost:4572')


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


@pytest.fixture(scope='function')
def put_user_items(dynamodb):
    """
    put user items
    """

    fixtures = [
        {
            'UserId': '0001'
        },
        {
            'UserId': '0002'
        }
    ]

    with dynamodb.Table(os.environ['USER_TABLE_NAME']).batch_writer() as batch:
        for fixture in fixtures:
            batch.put_item(Item=fixture)


@pytest.fixture(scope='function')
def create_bucket(s3, request):
    """
    create bucket fixture
    """

    bucket_name = os.environ['ATTENDANCE_DATA_BUCKET_NAME']
    s3.create_bucket(Bucket=bucket_name)

    def delete_bucket():
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete()
        bucket.delete()
    request.addfinalizer(delete_bucket)


@pytest.fixture(scope='function')
def put_bucket_items(s3, request):
    """
    put object in bucket fixture
    """

    bucket_name = os.environ['ATTENDANCE_DATA_BUCKET_NAME']

    for i in request.param:
        key = i[0]
        file = i[1]

        rel_path = f'fixtures/{file}'
        filename = str(Path(__file__).parent.joinpath(rel_path).resolve())

        s3.Object(bucket_name, key).upload_file(filename)
