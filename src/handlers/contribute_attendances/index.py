from fetch_report_service import FetchReportService
from post_message_service import PostMessageService


def handler(event, context):
    report = FetchReportService().fetch_report()
    PostMessageService().post_message(report)
