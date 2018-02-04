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
