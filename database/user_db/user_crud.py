import user_db_models as model

from model.user import User
from model.comment import Comment

from sqlalchemy.orm import Session
from datetime import datetime


# all the crud (create, read, update and delete) methos to ensure data persistance

# #####################USER##################################################"""


def create_user(db: Session, user: User):
    """
    ask db to create a new user
    :param db:
    :param user: a dict with values for new user attributes
    :return: the new user create in db
    """
    new_user = model.User(
        username=user.username,
        password=user.password,
        admin=user.admin,
        creation_date=user.creation_date
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_name(db: Session, username: str):
    """
    get a user in db, with his name
    :param db: session
    :param name: str, name of the user
    :return: a user
    """
    return db.query(model.User).filter(model.User.username == username).first()


def get_user_by_id(db: Session, id: int):
    """
    get a user in db, with his id
    :param db: session
    :param id: int, id of the searched user
    :return: a user
    """
    return db.query(model.User).filter(model.User.id_user == id).first()




# ###########################################COMMENT##################################################""


def create_comment(db: Session, new_comment: Comment):
    """
    create a new comment in db
    :param db: session
    :param newcomment: dict, information to create the new comment
    :return: the new comment saved in db
    """
    comment = model.Comment(
        content=new_comment.content,
        creation_date= new_comment.creation_date,
        id_user=new_comment.id_user,
    )
    db.add(comment)
    db.commit()
    return comment


def get_all_comment(db: Session, skip: int = 0, limit: int = 100):
    """
    get the list of all the comment in db
    :param db: session
    :param skip:
    :param limit: len max of the list
    :return: a list of comments
    """
    return db.query(model.Comment).offset(skip).limit(limit).all()


