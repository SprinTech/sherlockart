import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


def test_create_user(test_init_db):
    response = test_init_db.post("/user/", json={"username": "François", "password": '1234'})

    if response.status_code == 400:
        print("400")

    elif response.status_code == 200:
        print("200")
        data = response.json()
        assert data["username"] == "François"
        assert data["password"] == "1234"