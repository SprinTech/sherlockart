import mysql.connector
from sqlalchemy import create_engine

from conf.conf_connect import mysql_user, mysql_host, mysql_password


# METHODS TO ACCESS AND WORK WITH MYSQL


def connect_to_mysql():
    """
    to create a connection to mysql
    :return: a connection object
    """
    mysql_connection = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        auth_plugin='mysql_native_password')
    return mysql_connection


def create_db(mysql_connection, user_database_name):
    """
    create the database if not exists
    :param mysql_connection: a connection object
    :param database_name: the name of the new database
    :return:nan
    """
    cursor = mysql_connection.cursor()
    cursor.execute("""CREATE DATABASE IF NOT EXISTS """ + user_database_name)
    cursor.execute("""USE """ + user_database_name)
    return cursor


def connect_to_db(user_database_name):
    """
    connection to database
    :return: a connection object
    """
    new_database_name = user_database_name
    db_connection = create_engine(
        'mysql+mysqlconnector://{0}:{1}@localhost/{2}'.format(mysql_user, mysql_password, new_database_name))
    return db_connection
