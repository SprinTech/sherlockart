import pytest
import asyncio


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

test_database_name = "test_secret_diary"


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

    models.Base.metadata.create_all(bind=db_connection)

    populate_table = """
    INSERT INTO customer(name,firstname, information)
    VALUES("de smedt","marie", "test")
    """
    db_cursor.execute(populate_table)
    session_make.commit()

    yield db_cursor
