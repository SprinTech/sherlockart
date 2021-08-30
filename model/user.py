import datetime
from comment import Comment

import sys

sys.path.insert(1, 'api')
from api import crud


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.admin = False
        self.creation_date = datetime.today()
        self.modification_date = False
        self.deleted_date = False

    def create_new_comment(text, id_user):
        new_comment = Comment(text, id_user)
        crud.create_comment(new_comment)
