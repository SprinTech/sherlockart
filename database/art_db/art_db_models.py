import sys
sys.path.insert(0,'/home/apprenant/vscode_projects/sherlock-art')

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DATE
from database.art_db.art_db_connect import Base



class Current(Base):
    __tablename__ = "current"

    id_current = Column(Integer, primary_key=True, index=True)

    name = Column(String(25), unique=False, index=True)
    period = Column(String(25), unique=False, index=True)
    information = Column(Text, unique=False)
    artistes = Column(String(255), unique=False, index=True)

    creation_date = Column(DateTime, unique=False, index=True)
    modification_date = Column(DateTime, unique=False, index=True)
    deleted_date = Column(DateTime, unique=False, index=True)

    artwork = relationship("Artwork", back_populates="artwork_current")


class Artwork(Base):
    __tablename__ = "artwork"

    id_artwork = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), unique=False, index=True)
    url = Column(String(255), unique=False, index=True)
    
    creation_date = Column(DateTime, unique=False, index=True)
    modification_date = Column(DateTime, unique=False, index=True)
    deleted_date = Column(DateTime, unique=False, index=True)

    id_current = Column(Integer, ForeignKey('current.id_current'))

    artwork_current = relationship("Current", back_populates="artwork")
