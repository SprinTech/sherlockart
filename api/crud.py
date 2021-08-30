from sqlalchemy.orm import Session
from database.user_db import user_db_models as models
import schemas


# ---- USER ---- #
def get_user_by_username(db: Session, username: str, password: str):
    return db.query(models.User).filter(models.User.username == username,
                                        models.User.password == password).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    password = user.password
    db_user = models.User(
        username=user.username,
        password=password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db, user_id: int):
    return db.get(models.User, user_id)


# --- COMMENTS --- #
def create_comment(db: Session, comment: schemas.CommentCreate, id_user: int):
    db_comment = models.Comment(content=comment.content, id_user=id_user)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_by_user_id(db: Session, user_id: int):
    return db.query(models.Comment).filter(models.Comment.user_id == user_id).all()


def get_all_comment(db: Session, skip: int = 0, limit: int = 100):
    """
    Get the list of all the comment in db

    :param db: session
    :param skip:
    :param limit: len max of the list

    :return: a list of comments
    """
    return db.query(models.Comment).offset(skip).limit(limit).all()


def get_user_id(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
