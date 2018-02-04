import os

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
    s3 fixture
    """

    return boto3.resource('s3', endpoint_url='http://localhost:4572')


@pytest.fixture(scope='function')
def create_attendance_bucket(s3, request):
    """
    create s3 bucket
    """

    bucket_name = os.environ['ATTENDANCE_DATA_BUCKET_NAME']
    s3.create_bucket(Bucket=bucket_name)

    def delete_attendance_bucket():
        bucket_name = os.environ['ATTENDANCE_DATA_BUCKET_NAME']
        bucket = s3.Bucket(bucket_name)
        bucket.delete()
    request.addfinalizer(delete_attendance_bucket)
