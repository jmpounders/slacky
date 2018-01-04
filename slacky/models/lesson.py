import uuid
import datetime

from ..common.database import Database
from .cfu import CFUMessage

class Lesson(object):
    def __init__(self, user, title, user_id, _id=None):
        self.user = user
        self.user_id = user_id
        self.title = title
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_cfu(self, title, message):
        cfu = CFUMessage(title, message, self.user_id)
        cfu.save_to_mongo()

    def get_cfus(self):
        return CFUMessage.find_by_lesson_id(self._id)

    def save_to_mongo(self):
        Database.insert(collection='lessons', data=self.json())

    def update(self, new_data):
        Database.update('lessons', {'_id': self._id}, new_data)

    def json(self):
        return {
            'user': self.user,
            'user_id': self.user_id,
            'title': self.title,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        lesson_data = Database.find_one(collection='lessons',
                                        query={'_id': id})
        return cls(**lesson_data)

    @classmethod
    def delete_from_mongo(cls, _id):
        lesson_data = Database.find_one(collection='lessons',
                                        query={'_id': _id})
        Database.delete('lessons', lesson_data)

        cfus = CFUMessage.find_by_lesson_id(_id)
        for cfu in cfus:
            CFUMessage.delete_from_mongo(cfu._id)

    @classmethod
    def update_mongo(cls, id, new):
        pass

    @classmethod
    def find_by_user_id(cls, user_id):
        lessons = Database.find(collection='lessons',
                                query={'user_id': user_id})
        return [cls(**lesson_data) for lesson_data in lessons]



