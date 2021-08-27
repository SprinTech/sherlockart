from fastapi import FastAPI

import sys

sys.path.insert(0, 'API_1')

import schemas
import crud
from database.user_db.user_db_connect import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/user/')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.
    Access: For any people

    :return user account information
    """
    db_user = crud.get_user_by_username(db, username=user.username, password=user.password)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


# requête à modifier
@app.get("/user/")
def read_user(username: str, password: str, db: Session = Depends(get_db)):
    """
    Get users informations by user_id
    Access: Only for administrator

    :param user_id: id of user (int)

    :return information about user specified

    """
    db_user = crud.get_user_by_username(db, username=username, password=password)
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=403, detail="User not registered")


@app.post("/comments/")
def create_comment(comment: schemas.CommentCreate, username: str, db: Session = Depends(get_db)):
    """
    Post a comment.
    Access: Only of the user who's connected

    :param comment: user comment (string)

    :return
    """
    user = crud.get_user_id(db, username)
    return crud.create_comment(db, comment, user.id_user)


@app.get("/comments/")
def read_all_comment(db: Session = Depends(get_db)):
    comments = crud.get_all_comment(db)
    if len(comments) > 0:
        return comments
    else:
        raise HTTPException(status_code=403, detail="no comments")
