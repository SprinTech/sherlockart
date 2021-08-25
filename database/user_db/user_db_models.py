from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Enum, Text
from sqlalchemy.orm import relationship

import sys

sys.path.insert(1, 'database/user_db')
from user_db_connect import Base


class Role(str, Enum):
    admin = 'admin'
    user = 'user'


class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    hashed_password = Column(String(100))
    disabled = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    creation_date = Column(DateTime, unique=False, index=True)
    modification_date = Column(DateTime, unique=False, index=True)
    deleted_date = Column(DateTime, unique=False, index=True)

    user_comment = relationship("Comment", back_populates="user")


class Comment(Base):
    __tablename__ = "comment"

    id_comment = Column(Integer, primary_key=True, index=True)
    content = Column(String(25), unique=False, index=True)
    creation_date = Column(DateTime, unique=False, index=True)
    modification_date = Column(DateTime, unique=False, index=True)
    deleted_date = Column(DateTime, unique=False, index=True)
    id_user = Column(Integer, ForeignKey('user.id_user'))

    user = relationship("User", back_populates="user_comment")
