import os

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
