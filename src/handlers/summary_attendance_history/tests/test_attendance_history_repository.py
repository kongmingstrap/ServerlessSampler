import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

import pytest

from attendance_history_repository import AttendanceHistoryRepository


class TestMergedData(object):
    @pytest.mark.usefixtures('create_bucket')
    @pytest.mark.parametrize(
        'now_time_string', [
            ('2018/02/02 02:10:10')
        ])
    def test_dose_not_exist(self, s3_client, now_time_string):
        repository = AttendanceHistoryRepository()
        repository.s3 = s3_client

        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.strptime(now_time_string, '%Y/%m/%d %H:%M:%S')
        target_timestamp = datetime.fromtimestamp(
            timestamp=dt.timestamp(), tz=JST)

        repository.merged_data(target_timestamp)

    @pytest.mark.parametrize(
        'now_time_string', [
            ('2018/02/02 02:10:10')
        ])
    def test_bucket_dose_not_exist(self, s3_client, now_time_string):
        repository = AttendanceHistoryRepository()
        repository.s3 = s3_client

        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.strptime(now_time_string, '%Y/%m/%d %H:%M:%S')
        target_timestamp = datetime.fromtimestamp(
            timestamp=dt.timestamp(), tz=JST)

        with pytest.raises(Exception):
            repository.merged_data(target_timestamp)

    @pytest.mark.usefixtures('create_bucket')
    @pytest.mark.parametrize(
        'put_bucket_items, now_time_string, source_file', [
            (([
                ['2018/01/31/14/2018-01-31-14-01', '2018-01-31-14-01'],
                ['2018/01/31/14/2018-01-31-14-02', '2018-01-31-14-02'],
                ['2018/01/31/15/2018-01-31-15-01', '2018-01-31-15-01'],
                ['2018/01/31/15/2018-01-31-15-02', '2018-01-31-15-02'],
                ['2018/01/31/23/2018-01-31-23-01', '2018-01-31-23-01'],
                ['2018/01/31/23/2018-01-31-23-02', '2018-01-31-23-02'],
                ['2018/02/01/00/2018-02-01-00-01', '2018-02-01-00-01'],
                ['2018/02/01/00/2018-02-01-00-02', '2018-02-01-00-02'],
                ['2018/02/01/14/2018-02-01-14-01', '2018-02-01-14-01'],
                ['2018/02/01/14/2018-02-01-14-02', '2018-02-01-14-02'],
                ['2018/02/01/15/2018-02-01-15-01', '2018-02-01-15-01'],
                ['2018/02/01/15/2018-02-01-15-02', '2018-02-01-15-02']
            ]), '2018/02/02 02:10:10', '2018-02-01.json')
        ], indirect=['put_bucket_items'])
    def test_normal(self,
                    s3_client,
                    put_bucket_items,
                    now_time_string,
                    source_file):
        repository = AttendanceHistoryRepository()
        repository.s3 = s3_client

        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.strptime(now_time_string, '%Y/%m/%d %H:%M:%S')
        target_timestamp = datetime.fromtimestamp(
            timestamp=dt.timestamp(), tz=JST)

        merged_data = repository.merged_data(target_timestamp)

        assert merged_data is not None

        rel_path = f'fixtures/{source_file}'
        filename = str(Path(__file__).parent.joinpath(rel_path).resolve())

        with open(filename) as fp:
            assert merged_data == fp.read()


class TestPutData(object):
    @pytest.mark.usefixtures('create_bucket')
    @pytest.mark.parametrize(
        'now_time_string, source_file, dist_file', [
            ('2018/02/02 02:10:10',
             '2018-02-01.json',
             '2018/2018-02-01.json')
        ])
    def test_normal(self, s3_client, now_time_string, source_file, dist_file):
        repository = AttendanceHistoryRepository()
        repository.s3 = s3_client

        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.strptime(now_time_string, '%Y/%m/%d %H:%M:%S')
        target_timestamp = datetime.fromtimestamp(
            timestamp=dt.timestamp(), tz=JST)

        bucket_name = os.environ['HISTORY_DATA_BUCKET_NAME']
        key_prefix = os.environ['HISTORY_DATA_KEY_PREFIX']

        rel_path = f'fixtures/{source_file}'
        fixture_filename = str(
            Path(__file__).parent.joinpath(rel_path).resolve())

        with open(fixture_filename) as fp:
            repository.put_data(fp.read(), target_timestamp)

        object = s3_client.get_object(
            Bucket=bucket_name,
            Key=f'{key_prefix}{dist_file}')

        assert object.get('Body') is not None


class TestGetStartDate(object):
    @pytest.mark.parametrize('now_time_string, start_date_string', [
        ('2018/02/02 02:10:10', '2018/01/31 15:00:00'),
        ('2019/01/02 02:10:10', '2018/12/31 15:00:00'),
        ('2020/03/02 02:10:10', '2020/02/29 15:00:00')
    ])
    def test_normal(self, now_time_string, start_date_string):
        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.strptime(now_time_string, '%Y/%m/%d %H:%M:%S')
        target_timestamp = datetime.fromtimestamp(
            timestamp=dt.timestamp(), tz=JST)

        start_date = \
            AttendanceHistoryRepository()._get_start_date(target_timestamp)

        expected = datetime.strptime(start_date_string, '%Y/%m/%d %H:%M:%S')

        assert start_date == expected


class TestGetFinishDate(object):
    @pytest.mark.parametrize('now_time_string, finish_date_string', [
        ('2018/02/02 02:10:10', '2018/02/01 14:59:59'),
        ('2019/01/01 02:10:10', '2018/12/31 14:59:59'),
        ('2020/03/01 02:10:10', '2020/02/29 14:59:59')
    ])
    def test_normal(self, now_time_string, finish_date_string):
        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.strptime(now_time_string, '%Y/%m/%d %H:%M:%S')
        target_timestamp = datetime.fromtimestamp(
            timestamp=dt.timestamp(), tz=JST)

        finish_date = \
            AttendanceHistoryRepository()._get_finish_date(target_timestamp)

        expected = datetime.strptime(finish_date_string, '%Y/%m/%d %H:%M:%S')

        assert finish_date == expected


class TestGetDataFileKey(object):
    @pytest.mark.parametrize('now_time_string, expected', [
        ('2018/02/01 02:10:10', '2018/2018-01-31.json'),
        ('2019/01/01 02:10:10', '2018/2018-12-31.json'),
        ('2020/03/01 02:10:10', '2020/2020-02-29.json')
    ])
    def test_normal(self, now_time_string, expected):
        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.strptime(now_time_string, '%Y/%m/%d %H:%M:%S')
        target_timestamp = datetime.fromtimestamp(
            timestamp=dt.timestamp(), tz=JST)

        get_put_file_key = \
            AttendanceHistoryRepository()._get_data_file_key(target_timestamp)

        assert get_put_file_key == expected


class TestFetchTargetLists(object):
    @pytest.mark.parametrize('time_list, time_string', [
        (
            [
                '2018/01/31/15',
                '2018/01/31/16',
                '2018/01/31/17',
                '2018/01/31/18',
                '2018/01/31/19',
                '2018/01/31/20',
                '2018/01/31/21',
                '2018/01/31/22',
                '2018/01/31/23',
                '2018/02/01/00',
                '2018/02/01/01',
                '2018/02/01/02',
                '2018/02/01/03',
                '2018/02/01/04',
                '2018/02/01/05',
                '2018/02/01/06',
                '2018/02/01/07',
                '2018/02/01/08',
                '2018/02/01/09',
                '2018/02/01/10',
                '2018/02/01/11',
                '2018/02/01/12',
                '2018/02/01/13',
                '2018/02/01/14'
            ], '2018/02/02 02:10:10'
        ),
        (
            [
                '2018/12/31/15',
                '2018/12/31/16',
                '2018/12/31/17',
                '2018/12/31/18',
                '2018/12/31/19',
                '2018/12/31/20',
                '2018/12/31/21',
                '2018/12/31/22',
                '2018/12/31/23',
                '2019/01/01/00',
                '2019/01/01/01',
                '2019/01/01/02',
                '2019/01/01/03',
                '2019/01/01/04',
                '2019/01/01/05',
                '2019/01/01/06',
                '2019/01/01/07',
                '2019/01/01/08',
                '2019/01/01/09',
                '2019/01/01/10',
                '2019/01/01/11',
                '2019/01/01/12',
                '2019/01/01/13',
                '2019/01/01/14'
            ], '2019/01/02 02:10:10'
        ),
        (
            [
                '2020/02/28/15',
                '2020/02/28/16',
                '2020/02/28/17',
                '2020/02/28/18',
                '2020/02/28/19',
                '2020/02/28/20',
                '2020/02/28/21',
                '2020/02/28/22',
                '2020/02/28/23',
                '2020/02/29/00',
                '2020/02/29/01',
                '2020/02/29/02',
                '2020/02/29/03',
                '2020/02/29/04',
                '2020/02/29/05',
                '2020/02/29/06',
                '2020/02/29/07',
                '2020/02/29/08',
                '2020/02/29/09',
                '2020/02/29/10',
                '2020/02/29/11',
                '2020/02/29/12',
                '2020/02/29/13',
                '2020/02/29/14'
            ], '2020/03/01 02:10:10'
        ),
        (
            [
                '2020/02/29/15',
                '2020/02/29/16',
                '2020/02/29/17',
                '2020/02/29/18',
                '2020/02/29/19',
                '2020/02/29/20',
                '2020/02/29/21',
                '2020/02/29/22',
                '2020/02/29/23',
                '2020/03/01/00',
                '2020/03/01/01',
                '2020/03/01/02',
                '2020/03/01/03',
                '2020/03/01/04',
                '2020/03/01/05',
                '2020/03/01/06',
                '2020/03/01/07',
                '2020/03/01/08',
                '2020/03/01/09',
                '2020/03/01/10',
                '2020/03/01/11',
                '2020/03/01/12',
                '2020/03/01/13',
                '2020/03/01/14'
            ], '2020/03/02 02:10:10'
        )
    ])
    def test_normal(self, time_list, time_string):
        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.strptime(time_string, '%Y/%m/%d %H:%M:%S')
        target_timestamp = datetime.fromtimestamp(
            timestamp=dt.timestamp(), tz=JST)

        target_list = \
            AttendanceHistoryRepository()._fetch_target_lists(target_timestamp)

        assert len(target_list) == len(time_list)
        assert target_list == time_list
