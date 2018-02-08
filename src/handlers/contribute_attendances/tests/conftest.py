import os
from pathlib import Path

import boto3
import pytest


def pytest_runtest_setup():
    """
    Setup Lambda function
    """

    os.environ['ATTENDANCE_DATA_BUCKET_NAME'] = 'attendance-data'


@pytest.fixture(scope='session')
def s3():
    """
    s3 resource fixture
    """

    return boto3.resource('s3', endpoint_url='http://localhost:4572')


@pytest.fixture(scope='session')
def s3_client():
    """
    s3 client fixture
    """

    return boto3.client('s3', endpoint_url='http://localhost:4572')


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
