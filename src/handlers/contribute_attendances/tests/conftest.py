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
