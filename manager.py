#! /usr/bin/python
import sqlite3
import os
import datetime
import time
import hashlib
import pyperclip
import random
from config import config
from menu import menu
from string import *
from pathlib import Path
from rich.prompt import Prompt
from rich.console import Console

os.system("clear")
console = Console()

os.system("figlet -c -f Bloody 'Munseer' | lolcat")

def generate_password(length):
    sym = ";:/|#!$%^&*(){}[]"
    all = ascii_lowercase + ascii_uppercase + digits + sym
    r = random.sample(all, length)
    password = "".join(r)
    console.print(f"Your password is ready: [bold]{password}[/bold]")

def date():
    x = str(datetime.datetime.now().strftime("%H:%M:%S %b %d %Y"))
    return x

console.print(date().replace(":", "[blink]:[/blink]"))

def copy(text):
    pyperclip.copy(text)
    pyperclip.paste()

class Main:
    def set_details(self):
        if config != None:
            return "OK"
        else:
            master = Prompt.ask("Set a master password to use", password=True).strip()
            ver = Prompt.ask("Enter the password again", password=True).strip()
            if master != ver:
                console.print("Password Does not match. Try again...")
                self.set_details()
            else:
                key = self.md5_encoder(master)
                database = Prompt.ask("\nEnter path to your sqlite3 database file").strip()
                log = Prompt.ask("\nEnter path to a directory to save log")
                with open(f"{Path(__file__).resolve().parent}/config.py", "w") as f:
                    conf = f"""config = {{
    'KEY': '{key}',
    'PATH_TO_DATABASE': '{database}',
    'PATH_TO_LOG': '{log}'
}}"""
                    f.write(conf)
                    f.close()
                    console.print("Please Rerun The Script")
                    quit()

    def __init__(self):
        if self.set_details() != "OK":
            pass
        else:
            self.conn = sqlite3.connect(config["PATH_TO_DATABASE"])
            self.cur = self.conn.cursor()
            self.security()

    def md5_encoder(self, word):
        enc = hashlib.md5(word.encode()).hexdigest()
        return enc

    def fetch(self, app):
        apps = []
        usernames = []
        emails = []
        passwords = []
        try:
            self.cur.execute(f'SELECT * FROM PASSWORDS WHERE APPLICATION LIKE "%{app}%"')
            creds = self.cur.fetchall()
            for cred in creds:
                apps.append(cred[0])
                usernames.append(cred[1])
                emails.append(cred[2])
                passwords.append(cred[3])
            
            if len(apps) < 1:
                console.print("No creds found")
            else:
                if len(apps) == 1:
                    copy(cred[3])
                else:
                    pass
                for (a, b, c, d) in zip(apps, usernames, emails, passwords):
                    console.print(f'\nApplication     : [bold]{a}[/bold]')
                    console.print(f'Username        : [bold]{b}[/bold]')
                    console.print(f'Email/phone     : [bold]{c}[/bold]')
                    console.print(f'Password        : [bold]{d}[/bold]')
        except sqlite3.Error as e:
            console.print(e)
    
    def fetch_email(self, email):
        self.cur.execute(f"SELECT APPLICATION FROM PASSWORDS WHERE EMAIL LIKE '%{email}%'")
        apps = self.cur.fetchall()
        console.print(f"Found {len(apps)} apps linked to this email address\n")
        for app in apps:
            app = "".join(app)
            console.print(f"Application:  [bold]{app}[/bold]")

    def log(self, app, time, script):
        insertQuery = f"""INSERT INTO LOG VALUES (?, ?, ?)"""
        self.cur.execute(insertQuery, (app.capitalize(), time, script))
        self.conn.commit()
        self.conn.close()

    def new(self, app, user, email, password):
        try:
            copy(password)
            insertQuery = f"""INSERT INTO PASSWORDS VALUES (?, ?, ?, ?)"""
            self.cur.execute(insertQuery, (app.capitalize(), user, email, password))
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            console.print("Oops Something Went Wrong")


    def log_txt(self, app, time, script):
        with open(f'{config["PATH_TO_LOG"]}/logs.log', "a") as f:
            f.write(
                f"\nTime: {time} Script: {script} Application: {app.capitalize()}")
            f.close()

    def main(self):
        menu()
        option = int(input("\nSelect one option from menu: "))
        if option == 1:
            app = Prompt.ask("\nEnter the name of the application").strip()
            self.log_txt(app, date(), __file__)
            self.fetch(app)
            self.log(app, date(), __file__)
            pas = Prompt.ask("\nDo you need a new password", choices=["y", "n"], default="y")
            if pas != "y":
                pass
            else:
                generate_password(20)
        elif option == 2:
            email = Prompt.ask("Enter email address").strip()
            self.fetch_email(email)
        elif option == 3:
            app = Prompt.ask("\nEnter the name of the app").strip()
            user = Prompt.ask("Enter username of the application").strip()
            email = Prompt.ask("Enter the email address used for application").strip()
            password = Prompt.ask("Enter password of the application", password=True).strip()
            self.new(app, user, email, password)
        elif option == 4:
            exit()

    def security(self):
        i = 0
        inp = Prompt.ask("Enter password to unlock file", password=True).strip()
        enc = self.md5_encoder(inp)
        while enc != config["KEY"]:
            console.print("Access Denied!")
            i += 1
            if i >= 3:
                break
            else:
                inp = Prompt.ask("\nTry again", password=True).strip()
                enc = self.md5_encoder(inp)
        else:
            console.print("Access Granted")
            self.main()

if __name__ == "__main__":
    Main()

time.sleep(3)
os.system("clear")
