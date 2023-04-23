import os
import argparse
from dotenv import load_dotenv
import mysql.connector as sql

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
        db = sql.connect(
            host=os.environ.get('SQLHOST'),
            user=os.environ.get('SQLUSER'),
            password=os.environ.get('SQLPASSWORD'),
            database=os.environ.get('SQLDATABASE')
        );

        print(db)

        cursor = db.cursor()
        query = "SELECT * FROM transporters;"

        cursor.execute(query)

        rows = cursor.fetchall()

        # for row in rows:
        #     print(row)

        cursor.close()
        db.close()        


if __name__ == "__main__":
    main()