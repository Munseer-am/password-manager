import config
import sqlite3

def insert(app, user, email, password):
        try:
            pass_con = sqlite3.connect(config.database_file_path)
            cur = pass_con.cursor()
            insertQuery = f"""INSERT INTO PASSWORDS VALUES (?, ?, ?, ?)"""
            cur.execute(insertQuery, (app.capitalize(), user, email, password))
            pass_con.commit()
            pass_con.close()
        except Exception as e:
            print("Oops Something Went Wrong")