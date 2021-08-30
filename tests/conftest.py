import pytest
import asyncio
import os
import sys
import inspect
from fastapi.testclient import TestClient

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
print(parentdir)
sys.path.insert(0, parentdir)

from database.user_db import user_db_models as models
from database.user_db.user_db_connect import connect_to_mysql, connect_to_db,create_db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from conf.conf_connect import mysql_user, mysql_host, mysql_password

from api.api_routes_final import app, get_db

test_database_name = "testdb"


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

test_database_name = "testdb"


@pytest.mark.asyncio
@pytest.fixture(scope='module')
def test_init_db():
    mysql_connection = connect_to_mysql()

    create_db(mysql_connection, test_database_name)

    engine = connect_to_db(test_database_name)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()
    models.Base.metadata.create_all(bind=engine)


    def override_get_db():
        """Activate testing session"""
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()


    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    yield client   








# def session_make():
#     db_connection = connect_to_db(test_database_name)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_connection)
#     db = SessionLocal()
#     yield db


# @pytest.mark.asyncio
# @pytest.fixture(scope='module')
# def init_db(event_loop, session_make):
#     mysql_connection = connect_to_mysql()
#     db_cursor = create_db(mysql_connection, test_database_name)
#     db_connection = connect_to_db(test_database_name)
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_connection)

#     Base = declarative_base()
#     models.Base.metadata.create_all(bind=db_connection)

#     populate_table = """
#     INSERT INTO user(name,hashed_password)
#     VALUES("test","1234")
#     """
#     db_cursor.execute(populate_table)
#     session_make.commit()

#     yield db_cursor

    db_cursor.execute(populate_table)



