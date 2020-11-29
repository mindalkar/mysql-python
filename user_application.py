"""
Note - Execute it with python3
"""

import getpass
from mysql_connector import Connector
import mysql.connector.errors as mysql_exception


if __name__ == '__main__':

    mysql_user = input("Enter mysql Username: ").strip()
    mysql_password = getpass.getpass("Enter mysql Password: ").strip()
    #mysql_db = input("Enter mysql DB: ").strip()
    mysql_db = 'user_management'

    try:
        obj = Connector(mysql_user, mysql_password, mysql_db)
    except mysql_exception.ProgrammingError as e:
        print(e)
        exit()

    while(True):
        choice = input("\nEnter choice:\n1. Show Users list\n"
                       "2. Register new user\n"
                       "3. Exit\n")
        if choice == '1':

            admin_user = input("Enter admin username: ").strip()
            admin_password = getpass.getpass("Enter admin Password: ").strip()

            cmd = "SELECT * FROM {name}".format(name='admin_users')
            obj.mycursor.execute(cmd)

            correct_admin_credentials = False
            myresult = obj.mycursor.fetchall()
            for x in myresult:
                if x[0] == admin_user and x[1] == admin_password:
                    correct_admin_credentials = True
            if not correct_admin_credentials:
                print('Invalid admin credentials\n')
                continue
            print('Below are user details:-')
            print(obj.show_table_records('users'))

        elif choice == '2':
            record = {}
            print('\nPlease enter below details to register a new user-')
            record['username'] = input("Enter Username: ").strip()
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

            record['first_name'] = input("Enter user first name: ").strip()
            record['last_name'] = input("Enter user last name: ").strip()
            record['gender'] = input("Enter gender: ").strip()
            record['DOB'] = input("Enter D.O.B(yyyy-mm-dd): ").strip()
            obj.insert_into_table('users', record)

        elif choice == '3':
            print('Thanks You!!!!')
            break
