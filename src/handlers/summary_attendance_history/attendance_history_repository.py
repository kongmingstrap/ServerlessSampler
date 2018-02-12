import os
from datetime import datetime, timedelta

import boto3


class AttendanceHistoryRepository(object):
    def __init__(self):
        self.s3 = boto3.client('s3')
        self._bucket_name = os.environ['HISTORY_DATA_BUCKET_NAME']
        self._key_prefix = os.environ['HISTORY_DATA_KEY_PREFIX']

    def merged_data(self, current_date, specified_day=1):
        """
        merged data
        """

        target_list = self._fetch_target_lists(current_date, specified_day)

        merged_data = ''

        for key in target_list:
            prefix = f'{self._key_prefix}{key}'

            result = self.s3.list_objects(
                Bucket=self._bucket_name,
                Prefix=prefix
            )
            contents = result.get('Contents')

            if contents is not None:
                for content in contents:
                    key = content.get('Key')

                    object = self.s3.get_object(
                        Bucket=self._bucket_name,
                        Key=key)
                    body = object.get('Body').read()

                    merged_data = merged_data + body.decode('utf-8')

        return merged_data

    def put_data(self, body_data, current_date):
        """
        s3 put data
        """

        key = self._get_data_file_key(current_date)

        self.s3.put_object(
            Bucket=self._bucket_name,
            Key=f'{self._key_prefix}{key}',
            Body=body_data
        )

    def _get_start_date(self, timestamp, specified_day=1):
        yesterday = timestamp - timedelta(days=specified_day)
        yesterday_midnight = yesterday.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0)

        return datetime.utcfromtimestamp(yesterday_midnight.timestamp())

    def _get_finish_date(self, timestamp):
        yesterday = timestamp - timedelta(days=1)
        yesterday_finish = yesterday.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=0)

        return datetime.utcfromtimestamp(yesterday_finish.timestamp())

    def _get_data_file_key(self, timestamp):
        target_at = self._get_finish_date(timestamp)

        prefix = target_at.strftime('%Y')
        file_name = target_at.strftime('%Y-%m-%d')

        return f'{prefix}/{file_name}.json'

    def _fetch_target_lists(self, current_date, specified_day=1):
        dt = self._get_start_date(current_date, specified_day)

        def filename(number):
            t = dt + timedelta(hours=number)
            return t.strftime('%Y/%m/%d/%H')

        return [filename(i) for i in range(0, specified_day * 24)]
