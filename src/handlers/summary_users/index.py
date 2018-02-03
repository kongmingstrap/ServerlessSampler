from send_report_service import SendReportService
from summary_users_service import SummaryUsersService


def handler(event, context):
    report = SummaryUsersService().summary_report()
    SendReportService().send_report(report)
