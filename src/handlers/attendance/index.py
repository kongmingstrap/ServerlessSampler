from user_factory import UserFactory
from attendance_service import AttendanceService


def handler(event, context):
    http_method = event.get('httpMethod')

    if http_method == 'PUT':
        user = UserFactory().from_event(event)
        AttendanceService().send_report(user)
    else:
        print(f'Method Not Allowed: {http_method}')

    return {}
