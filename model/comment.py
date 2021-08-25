import datetime


class Comment:
  def __init__(self, content, id_user):
    self.content = content
    self.id_user = id_user
    self.creation_date = datetime.today()
    self.modification_date = None
    self.deleted_date = None

