import sys
sys.path.insert(0,'/home/apprenant/vscode_projects/sherlock-art')

from database.db_utils import connect_to_mysql, create_db, connect_to_db
from conf.conf_connect import art_database_name
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# FIRST FILE TO RUN TO CONNECT TO MYSQL AND TO CREATE DATABASE


# connect to mysql
mysql_connection = connect_to_mysql()

# create db if not exist
create_db(mysql_connection, art_database_name)

# connect to database
db_connection = connect_to_db(art_database_name)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_connection)

Base = declarative_base()