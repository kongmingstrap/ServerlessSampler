from attendance_repository import AttendanceRepository


class AttendanceService(object):
    def send_report(self, user):
        """
        send user data
        :param user:
        :return:
        """
        AttendanceRepository().put_user(user)
