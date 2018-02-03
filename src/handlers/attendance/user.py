class User(object):
    def __init__(self, user_id, place, attendance):
        self.user_id = user_id
        self.place = place
        self.attendance = attendance

    def user_data(self):
        """
        user data dictonary
        """
        body = {
            'UserId': self.user_id,
            'Attendance': self.attendance,
            'Place': self.place
        }
        return body
