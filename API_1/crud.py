from sqlalchemy.orm import Session
from database.user_db import user_db_models as models
import schemas
from security import pwd_context
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

SECRET_KEY = "b0a08b8aedbfc2d7b98113e72abb8748555d7173e876cadbdadd62d703cf4bce"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # hashed_password = pwd_context.hash(user.password)
    hashed_password = user.password
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def delete_user(db: Session, db_user:models.User):
#     db.delete(db_user)
#     db.commit()
#     return "Successfully deleted"


# def update_user(db : Session, db_user : models.User, new_username : str):
#     db_user.username = new_username
#     db.commit()
#     db.refresh(db_user)
#     return "Successfully updated!"


# def update_user_self(db: Session, current_user: schemas.User, user_update: schemas.UserUpdate):
#     db_user = get_user(db, current_user.id)
#     db_user.username = user_update.new_username
#     db_user.hashed_password = pwd_context.hash(user_update.password)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def verify_password(plain_password, hashed_password):
    # return pwd_context.verify(plain_password, hashed_password)
    return True


def get_password_hash(password):
    # return pwd_context.hash(password)
    return password


def get_user(db, user_id: int):
    return db.get(models.User, user_id)


def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    return user


def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(description=comment.description, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    print(db_comment)
    return db_comment


def get_comments_by_user_id(db: Session, user_id: int):
    return db.query(models.Comment).filter(models.Comment.user_id == user_id).all()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_all_comment(db: Session, skip: int = 0, limit: int = 100):
    """
    get the list of all the comment in db
    :param db: session
    :param skip:
    :param limit: len max of the list
    :return: a list of comments
    """
    return db.query(models.Comment).offset(skip).limit(limit).all()
