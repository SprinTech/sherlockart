from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from API_1.api_routes_final import app, get_db
from conf.conf_connect import mysql_user, mysql_password, user_database_name

engine = create_engine('mysql+mysqlconnetor://{0}:{1}@localhost/{2}'.format(mysql_user, mysql_password, user_database_name))

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Activate testing session"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_user():
    response = client.post("/user/", json={"username": "Jacques", "password": '1234'})
    assert response.status_code == 200
    data = response.json()
    assert data["mail"] == "Jacques"
    assert data["phone"] == "1234"
    assert "id" in data
    user_id = data['id']
