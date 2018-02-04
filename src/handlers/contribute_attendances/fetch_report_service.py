from fetch_report_repository import FetchReportRepository


class FetchReportService(object):
    def fetch_report(self):
        """
        send users data
        :param user:
        :return:
        """

        report = FetchReportRepository().fetch_report()

        return report
