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
from database.user_db.user_db_connect import connect_to_mysql, connect_to_db, create_db
from sqlalchemy.orm import sessionmaker

from api.api_routes_final import app, get_db

test_database_name = "testdb"


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
@pytest.fixture(scope='module')
def test_init_db():
    mysql_connection = connect_to_mysql()

    create_db(mysql_connection, test_database_name)

    engine = connect_to_db(test_database_name)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
