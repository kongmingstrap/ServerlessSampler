import os
import json
import boto3


s3 = boto3.resource('s3')


class PutReportRepository(object):
    def __init__(self):
        self._s3 = s3

    def put_report(self, report):
        """
        put report data
        """
        try:
            bucket_name = os.environ['ATTENDANCE_DATA_BUCKET_NAME']
            json_key = 'report.json'
            object = self._s3.Object(bucket_name, json_key)
            object.put(Body = json.dumps(report))
        except Exception as e:
            print('Exception: {e}'.format(e))
