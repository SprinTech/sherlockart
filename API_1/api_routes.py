from datetime import timedelta
from typing import List, Optional
from pydantic import BaseModel

import sys

sys.path.insert(0, 'API_1')

from fastapi import Depends, HTTPException, status
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import crud
import schemas
from crud import create_access_token, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from database.user_db import user_db_models as models
from database.user_db.user_db_connect import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Permit to verify if the person who want to connect has an account
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
        print(token_data)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    """
    Return if user is active
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_admin_user(admin_user: models.User = Depends(get_current_active_user)):
    """
    Return if user is admin
    """
    if admin_user.admin:
        return admin_user
    raise HTTPException(status_code=400, detail="User not admin!")


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.
    Access: For any people

    :return user account information
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               admin: models.User = Depends(get_admin_user)):
    """
    Get users informations.
    Access: Only for administrator

    :param skip: number of user to skip since 0 (0 by default)
    :param limit: maximum number of users to show

    :return list of users stored in database
    """
    if admin:
        users = crud.get_users(db, skip=skip, limit=limit)
        return users
    else:
        raise HTTPException(status_code=403, detail="Operation not permitted")


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), admin: models.User = Depends(get_admin_user)):
    """
    Get users informations by user_id
    Access: Only for administrator

    :param user_id: id of user (int)

    :return information about user specified
    """
    if admin:
        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    else:
        raise HTTPException(status_code=403, detail="Operation not permitted")


@app.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login to my profile.
    Access: For users who have an account
    """
    print("login_for_access_token")
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/comments", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_active_user)):
    """
    Post a comment.
    Access: Only of the user who's connected

    :param comment: user comment (string)

    :return
    """
    return crud.create_comment(db, comment, current_user.id)


@app.get("/comment", response_model=List[schemas.Comment])
def read_comment(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Get all the comments a user posted
    Access: Only of the user who's connected
    """
    if current_user:
        db_comment = crud.get_comments_by_user_id(db, user_id=current_user.id)
        if db_comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        return db_comment
    else:
        raise HTTPException(status_code=403, detail="Operation not permitted")


@app.get("/comments", response_model=List[schemas.Comment])
def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
      Get users informations.
      Access: Only for administrator
      """
    comments = crud.get_all_comment(db, skip=skip, limit=limit)
    if len(comments) > 0:
        return comments
    else:
        raise HTTPException(status_code=403, detail="no comments")


class Client(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


def fake_decode_token(token):
    return Client(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/client/me")
async def read_users_me(current_client: Client = Depends(get_current_user)):
    return current_client
