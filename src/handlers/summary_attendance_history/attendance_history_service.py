from attendance_history_repository import AttendanceHistoryRepository


class AttendanceHistoryService(object):
    def summary_report(self, current_date, specified_day=1):
        repository = AttendanceHistoryRepository()

        try:
            merged_data = repository.merged_data(current_date, specified_day)

            repository.put_data(
                body_data=merged_data,
                current_date=current_date
            )
        except Exception as e:
            print(f'Exception: {e}')
