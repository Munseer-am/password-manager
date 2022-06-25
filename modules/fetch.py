import config
import sqlite3

def creds(self, app):
        # creating list for storing passwords
        # list for application
        apps = []
        # list for usernames
        usernames = []
        # list for emails
        emails = []
        # list for passwords
        passwords = []
        # exception handling
        try:
            pass_con = sqlite3.connect(config.database_file_path)
            cur = pass_con.cursor()
            # executing SQL command
            cur.execute(f'SELECT * FROM PASSWORDS WHERE APPLICATION LIKE "%{app}%"')
            # fetching creds
            creds = cur.fetchall()
            # appending creds to list using for loop
            for cred in creds:
                apps.append(cred[0])
                usernames.append(cred[1])
                emails.append(cred[2])
                passwords.append(cred[3])

            if app == "":
                print("Invalid Input")
            elif len(apps) == 0:
                print("Invalid Input")
            else:
                # iterating through multiple list at same time
                for (a, b, c, d) in zip(apps, usernames, emails, passwords):
                    # printing the credentials
                    print(f'\nApplication     : {a}')
                    print(f'Username        : {b}')
                    print(f'Email/phone     : {c}')
                    print(f'Password        : {d}')
        # output invalid input for any sqlite3.error
        except sqlite3.Error as e:
            print(e)
