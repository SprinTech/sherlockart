import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


def test_create_user(test_init_db):
    response = test_init_db.post("/user/", json={"username": "Name1", "password": '1234'})

    if response.status_code == 400:
        print("400")

    elif response.status_code == 200:
        print("200")
        data = response.json()
        assert data["username"] == "Name1"
        assert data["password"] == "1234"

def test_get_user(test_init_db):
    response = test_init_db.get("/user/?username=Name1&password=1234")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "Name1"
    assert data["password"] == "1234"

def test_create_comment(test_init_db):
    response = test_init_db.post("/comments/?username=Name1", json={"content": "content test"})

    response.status_code == 200    
    data = response.json()
    assert data["content"] == "content test"
   

def test_get_comment(test_init_db):
    response = test_init_db.get("/comments/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["content"] == "content test"
    