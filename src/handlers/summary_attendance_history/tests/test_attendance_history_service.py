from datetime import datetime, timezone, timedelta

import pytest

from attendance_history_service import AttendanceHistoryService
from attendance_history_repository import AttendanceHistoryRepository


class TestSummaryReport(object):
    @pytest.mark.parametrize(
        'now_time_string', [
            ('2018/02/02 02:10:10')
        ])
    def test_normal(self, now_time_string, monkeypatch):
        def put_data_patched(*args, body_data, current_date):
            pass

        monkeypatch.setattr(
            AttendanceHistoryRepository,
            'merged_data', lambda *_: None)
        monkeypatch.setattr(
            AttendanceHistoryRepository,
            'put_data', put_data_patched)

        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.strptime(now_time_string, '%Y/%m/%d %H:%M:%S')

        target = datetime.fromtimestamp(
            timestamp=dt.timestamp(), tz=JST)

        AttendanceHistoryService().summary_report(target)
