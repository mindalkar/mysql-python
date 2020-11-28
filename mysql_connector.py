"""
Package required - 
pip install mysql-connector-python
"""

import getpass
import mysql.connector
import mysql.connector.errors as mysql_exception

class Connector:
    def __init__(self, username, password, database, host="localhost"):

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


if __name__ == '__main__':

    mysql_user = raw_input("Enter mysql Username: ").strip()
    mysql_password = getpass.getpass("Enter mysql Password: ").strip()
    mysql_db = raw_input("Enter mysql DB: ").strip()

    try:
        obj = Connector(mysql_user, mysql_password, mysql_db)
    except mysql_exception.ProgrammingError as e:
        print(e)
        exit()

    while(True):
        choice = raw_input("\nEnter choice:\n1. Show table records\n"
                           "2. Insert user details into table\n"
                           "3. Exit\n")
        if choice == '1':
            print('Below are user details:-')
            print(obj.show_table_records('user_details'))

        elif choice == '2':
            record = {}
            print('Please enter below details to insert user')
            record['username'] = raw_input("Enter Username: ").strip()
            password_not_enterd = True
            attempt = 1
            while (password_not_enterd and attempt < 3):
                pass1 = getpass.getpass("Enter password for user: ").strip()
                pass2 = getpass.getpass("Re-enter password: ").strip()
                if pass1 == pass2:
                    record['password'] = pass1
                    password_not_enterd = False
                else:
                    print("\nPassword didn't matched\n")
                    if attempt == 2:
                        print("Number of attempts exceeded. Exiting!!!")
                        exit()
                attempt += 1

            record['first_name'] = raw_input("Enter user first name: ").strip()
            record['last_name'] = raw_input("Enter user last name: ").strip()
            record['gender'] = raw_input("Enter gender: ").strip()
            record['DOB'] = raw_input("Enter D.O.B(yyyy-mm-dd): ").strip()
            obj.insert_into_table('user_details', record)

        elif choice == '3':
            print('Thanks You!!!!')
            break
