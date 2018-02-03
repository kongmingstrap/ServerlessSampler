from put_report_repository import PutReportRepository


class SendReportService(object):
    def send_report(self, report):
        """
        send users data
        :param user:
        :return:
        """
        PutReportRepository().put_report(report)
