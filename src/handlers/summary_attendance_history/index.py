from datetime import datetime, timezone, timedelta

from attendance_history_service import AttendanceHistoryService


def handler(event, context):
    JST = timezone(timedelta(hours=+9), 'JST')
    current_date = datetime.now(tz=JST)

    AttendanceHistoryService().summary_report(current_date)
