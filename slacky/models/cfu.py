import uuid
from random import shuffle

from ..common.database import Database
from ..common.slack import Slack

class CFUMessage(object):
    def __init__(self, title, message, user_id, lesson_id, seed_emoji=None, _id=None):
        self.title = title
        self.message = message
        self.user_id = user_id
        self.lesson_id = lesson_id
        self.seed_emoji = [] if seed_emoji is None else seed_emoji
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='cfus', data=self.json())

    def json(self):
        return {'_id': self._id,
                'seed_emoji': self.seed_emoji,
                'user_id': self.user_id,
                'lesson_id': self.lesson_id,
                'title': self.title,
                'message': self.message}

    def post(self):
        if type(self.seed_emoji) is int:
            Slack.post_enumerated_response_message(self.title, self.message, self.seed_emoji)
        else:
            Slack.post_message(self.title, self.message)


    @classmethod
    def get_from_mongo(cls, _id):
        cfu_data = Database.find_one(collection='cfus', query={'_id':_id})
        return cls(**cfu_data)

    @classmethod
    def delete_from_mongo(cls, _id):
        cfu_data = Database.find_one(collection='cfus', query={'_id':_id})
        Database.delete('cfus', cfu_data)

    @classmethod
    def find_by_user_id(cls, user_id):
        cfus = Database.find(collection='cfus', query={'user_id': user_id})
        cfu_list = [cls(**cfu_data) for cfu_data in cfus]
        return cfu_list

    @classmethod
    def find_by_lesson_id(cls, lesson_id):
        cfus = Database.find(collection='cfus', query={'lesson_id': lesson_id})
        cfu_list = [cls(**cfu_data) for cfu_data in cfus]
        return cfu_list


class MultipleChoiceCFU(CFUMessage):
    def __init__(self, title, question, options, user_id, lesson_id, _id=None):
        CFUMessage.__init__(self,
                            title+" (multiple choice)",
                            self._make_message(question, options),
                            user_id, lesson_id, len(options), _id)

    def _make_message(self, question, options, shuffle_opts=False):
        message = question + '\n'

        if shuffle_opts:
            shuffle(options)

        for i, opt in enumerate(options):
            message += str(i+1) + '. ' + opt + '\n'

        return message


class FreeResponseCFU(CFUMessage):
    def __init__(self, title, question, user_id, lesson_id, _id=None):
        CFUMessage.__init__(self,
                            title+" (free response)",
                            question,
                            user_id, lesson_id, _id=_id)

