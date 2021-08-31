import csv

from database.user_db import user_db_models, user_db_connect
from database.user_db.user_db_connect import db_connection, SessionLocal
from database.user_db.user_db_models import User, Comment
from datetime import datetime


# create tables
def user_db_init():
    user_db_models.Base.metadata.create_all(bind=db_connection)


# fill the user database
def user_load_data(data_file_name):
    """
    fill the db with csv file
    """
    with open(data_file_name, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        list_data = list(reader)
        #print("list_data", list_data)

    # Create the session
    SessionLocal.configure(bind=db_connection)
    s = SessionLocal()

    try:
        for i in list_data:
            # print(i)
            record = User(**{
                'username': i[1],
                'password': i[2],
                'admin': True,
                'creation_date': datetime.today()
            })
            s.add(record)  # Add all the records
            s.commit()  # Attempt to commit all the records
    except:
        print("rollback")
        s.rollback()  # Rollback the changes on error
    finally:
        print("close")
        s.close()  # Close the connection


# fill the comment database 
def comment_load_data(data_file_name):
    """
    fill the db with csv file
    """
    with open(data_file_name, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        list_data = list(reader)
        # print("list_data", list_data)

    # Create the session
    SessionLocal.configure(bind=db_connection)
    s = SessionLocal()



    try:
        # print("liste:", list_data) 
        for i in list_data:
            print(i)
            record = Comment(**{
                'content': i[1],
                'id_user': i[2],
                'creation_date': datetime.today()
            })
            # print("record:", record)
            s.add(record)  # Add all the records
            s.commit()  # Attempt to commit all the records
    except:
        print("rollback")
        s.rollback()  # Rollback the changes on error
    finally:
        print("close")
        s.close()  # Close the connection
