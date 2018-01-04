import uuid

from flask import session

from ..common.database import Database
from .lesson import Lesson

class User(object):
    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one('users', {'username':username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one('users', {'_id':_id})
        if data is not None:
            return cls(**data)


    @staticmethod
    def login_valid(username, password):
        user = User.get_by_username(username)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, username, password):
        user = User.get_by_username(username)
        if user is None:
            # create user
            new_user = cls(username, password)
            new_user.save_to_mongo()
            return True
        else:
            return False


    @staticmethod
    def login(user_username):
        # Login_valid has already been called
        session['username'] = user_username
        return User.get_by_username(user_username)

    @staticmethod
    def logout():
        session['username'] = None

    def get_lessons(self):
        return Lesson.find_by_user_id(self._id)

    @staticmethod
    def new_lesson(title):
        lesson = Lesson(self.username, title, self._id)
        lesson.save_to_mongo()

    def json(self):
        return {'username': self.username,
                'password': self.password,
                '_id': self._id}

    def save_to_mongo(self):
        Database.insert('users', self.json())
