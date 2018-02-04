import os
import json
import boto3


class FetchReportRepository(object):
    def __init__(self):
        self.s3 = boto3.resource('s3')

    def fetch_report(self):
        """
        fetch report data
        """

        try:
            bucket_name = os.environ['ATTENDANCE_DATA_BUCKET_NAME']
            json_key = 'report.json'
            object = self.s3.Object(bucket_name, json_key)
            report = object.get()['Body'].read()

            return json.loads(report)
        except Exception as e:
            print('Exception: {e}'.format(e))
