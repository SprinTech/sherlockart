import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
print(parentdir)
sys.path.insert(0, parentdir)

from database.db_utils import connect_to_db, create_db, connect_to_mysql
from database.user_db import user_db_models as models

from conf.conf_connect import mysql_user, mysql_password

def test_create_user(test_init_db):
    response = test_init_db.post("/user/", json={"username": "François", "password": '1234'})

    if response.status_code == 400:
        print("400")

    elif response.status_code == 200:
        print("200")
        data = response.json()
        assert data["username"] == "François"
        assert data["password"] == "1234"
        assert "id_user" in data
        user_id = data['id_user']
    
   
        

  

