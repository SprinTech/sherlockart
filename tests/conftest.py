import pytest
import asyncio

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
print(parentdir)
sys.path.insert(0, parentdir)

from database.db_utils import connect_to_mysql, create_db, connect_to_db
from sqlalchemy.orm import sessionmaker
from database.user_db import user_db_models

test_database_name = "test_user_db"


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
@pytest.fixture(scope='module')
def session_make():
    db_connection = connect_to_db(test_database_name)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_connection)
    db = SessionLocal()
    yield db


@pytest.mark.asyncio
@pytest.fixture(scope='module')
def init_db(event_loop, session_make):
    mysql_connection = connect_to_mysql()
    db_cursor = create_db(mysql_connection, test_database_name)
    db_connection = connect_to_db(test_database_name)

    user_db_models.Base.metadata.create_all(bind=db_connection)

    populate_table = """
    INSERT INTO customer(name,firstname, information)
    VALUES("de smedt","marie", "tests")
    """
    db_cursor.execute(populate_table)
    session_make.commit()

    yield db_cursor
