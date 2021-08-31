import csv

from database.art_db.art_db_connect import db_connection, SessionLocal
from database.art_db import art_db_models
from database.art_db.art_db_models import Artwork, Current
from datetime import datetime


# create tables
def art_db_init():
    art_db_models.Base.metadata.create_all(bind=db_connection)


# fill the artwork database 
def artwork_load_data(data_file_name):
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

    # print("liste:", list_data)
    for i in list_data:
        # print(i)
        record = Artwork(**{
            'name': i[1],
            'url': i[3],
            'id_current': i[4],
            'creation_date': datetime.today()
        })
        # print("record:", record)
        s.add(record)  # Add all the records
        s.commit()  # Attempt to commit all the records

    # try:       
    #     # print("liste:", list_data) 
    #     for i in list_data:
    #         # print(i)
    #         record = Artwork(**{
    #             'name' : i[1],
    #             'url' :i[3],
    #             'id_current': i[4],
    #             'creation_date' : datetime.today()
    #         })
    #         # print("record:", record)
    #         s.add(record) #Add all the records
    #         s.commit() #Attempt to commit all the records
    # except:
    #     print("rollback")
    #     s.rollback() #Rollback the changes on error
    # finally:
    #     print("close")
    #     s.close() #Close the connection


# fill the current database
def current_load_data(data_file_name):
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
            # print(i)
            record = Current(**{
                'name': i[0],
                'information': i[1],
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
