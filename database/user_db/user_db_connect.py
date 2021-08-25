from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
sys.path.insert(0,'/home/apprenant/vscode_projects/sherlock-art')
from database.db_utils import connect_to_mysql, create_db, connect_to_db


from conf.conf_connect import user_database_name

# FIRST FILE TO RUN TO CONNECT TO MYSQL AND TO CREATE DATABASE


# connect to mysql
mysql_connection = connect_to_mysql()

# create db if not exist
create_db(mysql_connection, user_database_name)

# connect to database
db_connection = connect_to_db(user_database_name)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_connection)

Base = declarative_base()

