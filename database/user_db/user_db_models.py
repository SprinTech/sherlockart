from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DATE
import sys
sys.path.insert(0,'/home/apprenant/vscode_projects/sherlock-art')
from database.user_db.user_db_connect import Base


class User(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=False, index=True)
    password = Column(String(25), unique=False, index=True)
    admin = Column(Boolean, unique=False, index=True)
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
