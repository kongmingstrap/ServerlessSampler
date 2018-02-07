import json

from user import User


class UserFactory(object):
    def from_event(self, event):
        """
        create user model
        :param event:
        :return:
        """

        body = event.get('body')
        dict = json.loads(body)
        user_model = User(
            user_id=dict.get('user_id'),
            place=dict.get('place'),
            attendance=dict.get('attendance'))

        return user_model
