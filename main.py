import os
import argparse
from dotenv import load_dotenv
import mysql.connector as sql
from Browse import Browse
from AddUpdateRemove import AddUpdateRemove

class main:
    def __init__(self):
        load_dotenv()

        # Checks to see if the user is an admin
        parser = argparse.ArgumentParser(description='fungalBase CLI')
        parser.add_argument('-p', '--password', help='password for admin')

        args = parser.parse_args()

        adminStatus = 0
        if args.password == os.environ.get('ADMINPASSWORD'): adminStatus = 1

        # Connects to the database
        self.db = sql.connect(
            host=os.environ.get('SQLHOST'),
            user=os.environ.get('SQLUSER'),
            password=os.environ.get('SQLPASSWORD'),
            database=os.environ.get('SQLDATABASE')
        );


        cursor = self.db.cursor()
        while(True):
            if adminStatus: self.promptAdmin() 
            else: self.promptBrowse()
            
        # query = "SELECT * FROM transporters;"

        # cursor.execute(query)

        # rows = cursor.fetchall()

        # for row in rows:
        #     print(row)

        cursor.close()
        db.close()        


    def promptAdmin(self):
        choice = input('''
            What would you like to do?\n
            1. Browse database\n
            2. Add to database\n
            3. Remove from database\n
            4. Update database\n
            5. Exit\n
            ''')
        addUpdateRemover = AddUpdateRemove(self.db)
        if choice == '1':
            self.promptBrowse()
        elif choice == '2':
            addUpdateRemover.addSpecies()
        elif choice == '3':
            print("TODO remove")
        elif choice == '4':
            print("TODO update")
        elif choice == '5':
            exit()
        else:
            print('Invalid choice. Please try again.')
            self.promptAdmin()

    def promptBrowse(self):
        browse = Browse(self.db)
        browse.promptBrowse()

if __name__ == "__main__":
    main()
