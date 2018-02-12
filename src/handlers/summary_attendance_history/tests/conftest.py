import os

import boto3
import pytest

from pathlib import Path


def pytest_runtest_setup():
    os.environ['HISTORY_DATA_BUCKET_NAME'] = 'history-data'
    os.environ['HISTORY_DATA_KEY_PREFIX'] = 'attendance/'


@pytest.fixture(scope='session')
def s3():
    """
    endpoint to localhost
    """

    return boto3.resource('s3', endpoint_url='http://localhost:4572')


@pytest.fixture(scope='session')
def s3_client():
    """
    endpoint to localhost
    """

    return boto3.client('s3', endpoint_url='http://localhost:4572')


@pytest.fixture(scope='function')
def create_bucket(s3, request):
    """
    put object in bucket fixture
    """

    bucket_name = os.environ['HISTORY_DATA_BUCKET_NAME']
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

    bucket_name = os.environ['HISTORY_DATA_BUCKET_NAME']

    for i in request.param:
        key = i[0]
        file = i[1]

        key_prefix = os.environ['HISTORY_DATA_KEY_PREFIX']
        key_name = f'{key_prefix}{key}'

        rel_path = f'fixtures/{file}'
        filename = str(Path(__file__).parent.joinpath(rel_path).resolve())

        s3.Object(bucket_name, key_name).upload_file(filename)
