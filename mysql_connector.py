"""
Note - Execute it with python3

Package required - 
pip install mysql-connector-python
"""

import getpass
import mysql.connector
import mysql.connector.errors as mysql_exception

class Connector:
    def __init__(self, username, password, database='', host="localhost"):

        self.mydb = mysql.connector.connect(
          host=host,
          user=username,
          password=password,
          database=database
        )

        self.mycursor = self.mydb.cursor()

    def show_databases(self):
        """Return list of DBs"""
        self.mycursor.execute("SHOW DATABASES")

        db_list = []
        for db in self.mycursor:
            try:
                db_list.append(db[0])
            except:
                pass

        return db_list

    def create_database(self, db_name):
        """Create Database."""

        cmd = "CREATE DATABASE {name}".format(name=db_name)
        self.mycursor.execute(cmd)

    def create_table(self, table_name, table_details):
        """Create table in DB."""

        cmd = "CREATE TABLE {name} {body}".format(name=table_name, body=table_details)
        self.mycursor.execute(cmd)

    def show_table_records(self, table_name):
        """Return all record from table."""

        cmd = "SELECT * FROM {name}".format(name=table_name)
        self.mycursor.execute(cmd)

        myresult = self.mycursor.fetchall()

        users = {}
        for record in myresult:
            try:
                username = record[0]
                users[username] = {}
                users[username]['password'] = record[1]
                users[username]['first_name'] = record[2]
                users[username]['last_name'] = record[3]
                users[username]['gender'] = record[4]
                users[username]['DOB'] = record[5]
                users[username]['ID'] = record[6]
            except:
                pass

        return users

    def insert_into_table(self, table_name, record):
        """Insert into table."""

        sql = ("INSERT INTO {name} (username, password, "
               "first_name, last_name, sex, birth) VALUES (%s, %s, %s, %s, %s, %s)".format(name=table_name))

        username = record['username']
        password = record['password']
        first_name = record['first_name']
        last_name = record['last_name']
        gender = record['gender']
        DOB = record['DOB']

        val = (username, password, first_name, last_name, gender, DOB)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

