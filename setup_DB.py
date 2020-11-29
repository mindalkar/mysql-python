"""
Note - Execute it with python3
"""

import getpass
from mysql_connector import Connector

if __name__ == '__main__':

    mysql_user = input("Enter mysql Username: ").strip()
    mysql_password = getpass.getpass("Enter mysql Password: ").strip()

    try:
        obj = Connector(mysql_user, mysql_password)
    except mysql_exception.ProgrammingError as e:
        print(e)
        exit()

    #mysql_db = input("Enter name of Database which you to create: ").strip()
    mysql_db = 'user_management'

    # Create DB
    obj.create_database(mysql_db)

    print('\nDatabase created successfully!!!!')

    try:
        DB_obj = Connector(mysql_user, mysql_password, database=mysql_db)
    except mysql_exception.ProgrammingError as e:
        print(e)
        exit()

    # Create User table in DB
    table_name = 'users'
    table_details = ("(username VARCHAR(20) PRIMARY KEY, "
                     "password VARCHAR(20), first_name VARCHAR(20), "
                     "last_name VARCHAR(20), sex CHAR(1), birth DATE)")
    DB_obj.create_table(table_name, table_details)

    print('users table created successfully!!!!')

    # Create Admin table in DB
    table_name = 'admin_users'
    table_details = ("(username VARCHAR(20) PRIMARY KEY, "
                     "password VARCHAR(20))")
    DB_obj.create_table(table_name, table_details)

    print('Admin users table created successfully!!!!\n')

    print('Enter below details to create admin user:')
    admin_username = input("Enter Admin Username: ").strip()
    password_not_enterd = True
    attempt = 1
    while (password_not_enterd and attempt < 3):
        pass1 = getpass.getpass("Enter password for admin user: ").strip()
        pass2 = getpass.getpass("Re-enter password: ").strip()
        if pass1 == pass2:
            password_not_enterd = False
        else:
            print("\nPassword didn't matched\n")
            if attempt == 2:
                print("Number of attempts exceeded. Exiting!!!")
                exit()
        attempt += 1

    sql = "INSERT INTO admin_users (username, password) VALUES (%s, %s)"
    val = (admin_username, pass1)
    DB_obj.mycursor.execute(sql, val)
    DB_obj.mydb.commit()

    print('\nAdmin user created successfully!!!!')
