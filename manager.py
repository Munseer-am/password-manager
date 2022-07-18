#! /usr/bin/python3
import sqlite3
import os
import time
import random
import sys
import hashlib
import datetime
import pyperclip
import shutil
from string import *
from pathlib import Path
sys.path.insert(0, f"{os.path.expanduser('~')}/.config/manager/")
from config import config
from menu import menu
from cryptography.fernet import Fernet
from rich.prompt import Prompt
from rich.console import Console

start = time.time()
os.system("clear")

os.system("figlet -c -f Bloody 'Munseer' | lolcat")
console = Console()
x = str(datetime.datetime.now().strftime("%H:%M:%S %b %d %Y"))
console.print(x.replace(":", "[blink]:[/blink]"))

def generate_password(LENGTH):
    sym = ":;?/'@#$%^&*(){}[]~"
    all = ascii_lowercase + ascii_uppercase + digits + sym
    r = random.sample(all, LENGTH)
    password = "".join(r)
    return password

def md5_encoder(word):
    enc = hashlib.md5(word.encode()).hexdigest()
    return enc

def copy(text):
    pyperclip.copy(text)
    pyperclip.paste()

class Main:
    def __init__(self):
        self.conn = sqlite3.connect(f"{os.path.expanduser('~')}/.config/manager/db.sqlite3")
        self.cur = self.conn.cursor()
        if self.is_configured() != "OK":
            self.set_details()
        else:
            self.key = b'o5Tzcd1X5Cjnmp_0U6xmdGZBXfs6ARWZe-UdSaXQDBI='
            self.security()

    def is_configured(self):
        if config != None:
            return "OK"
        else:
            return "NO"

    def set_details(self):
        createTable = """CREATE TABLE IF NOT EXISTS Passwords (
            Application VARCHAR(100),
            Username VARCHAR(100),
            Email VARCHAR(100),
            Password VARCHAR
        );"""
        createLog = """CREATE TABLE IF NOT EXISTS Log (
            App VARCHAR(100),
            Time VARCHAR(100),
            Script VARCHAR
        )"""
        self.cur.execute(createTable)
        self.cur.execute(createLog)
        self.conn.commit()
        self.conn.close()
        master = Prompt.ask("Set a master password to use", password=True).strip()
        ver = Prompt.ask("Enter the password again", password=True).strip()
        if master != ver:
            console.print("Password Does not match. Try again...\n")
            self.set_details()
        else:
            key = md5_encoder(master)
            encryption_key = Fernet.generate_key()
            email = Prompt.ask("Enter your email address")
            if "@" not in email:
                console.print("Enter a valide email address\n")
                self.set_details()
            else:
                email = md5_encoder(email)
            with open(f"{os.path.expanduser('~')}/.config/manager/config.py", "w") as f:
                conf = f"""config = {{
    'KEY': '{key}',
    'ENCRYPTION_KEY': {encryption_key},
    'EMAIL': '{email}',
    'PATH_TO_DATABASE': '{os.path.expanduser("~")}/.config/manager/db.sqlite3',
    'PATH_TO_BACKUP': '{os.path.expanduser("~")}/.config/manager/backup/',
    'PATH_TO_LOG': '{os.path.expanduser("~")}/.config/manager/log/'
}}"""
                f.write(conf)
                f.close()
            console.print("Please Rerun The Script")
            quit()

    def security(self):
        i = 0
        inp = str(Prompt.ask("Enter password to unlock file", password=True)).strip()
        enc = md5_encoder(inp)
        while enc != config["KEY"]:
            i += 1
            console.print("Access Denied!")
            if i >= 3:
                break
            else:
                inp = str(Prompt.ask("\nTry again", password=True)).strip()
                enc = md5_encoder(inp)
        else:
            console.print("Access Granted!")
            self.main()

    def email_search(self, email):
        self.cur.execute(f"SELECT APPLICATION FROM PASSWORDS WHERE EMAIL LIKE '%{email}%'")
        apps = self.cur.fetchall()
        console.print(f"Found {len(apps)} apps connected to this email\n")
        for app in apps:
            app = "".join(app)
            console.print(f"Application: [bold]{app}[/bold]")


    def encrypt(self, password):
        key = config["ENCRYPTION_KEY"]
        enc = Fernet(key)
        out = enc.encrypt(password.encode("utf-8"))
        return out

    def decrypt(self, hash):
        key = config["ENCRYPTION_KEY"]
        dec = Fernet(key)
        out = dec.decrypt(hash)
        return out

    def add(self, app, username, email, password):
        insertQuery = """INSERT INTO PASSWORDS VALUES(?, ?, ?, ?)"""
        encrypt = self.encrypt(password)
        self.cur.execute(insertQuery, (str(app).title(), username, email, encrypt))
        self.conn.commit()
        self.conn.close()
        self.backup()
        console.print("Inserted Successfully")

    def backup(self):
        shutil.copyfile(config["PATH_TO_DATABASE"], f'{config["PATH_TO_BACKUP"]}/backup.db')

    def log_txt(self, app, time, script):
        with open(f'{config["PATH_TO_LOG"]}/logs.log', "a") as f:
            f.write(
                f"\nTime: {time} Script: {script} Application: {app.capitalize()}")
            f.close()

    def log(self, app, time, script):
        insertQuery = f"""INSERT INTO LOG VALUES (?, ?, ?)"""
        self.cur.execute(insertQuery, (app.capitalize(), time, script))
        self.conn.commit()
        self.conn.close()

    def fetch(self, app):
        self.cur.execute(f"SELECT * FROM PASSWORDS WHERE APPLICATION LIKE '%{app}%'")
        creds = self.cur.fetchall()
        if len(creds) == 0:
            console.print("No Creds Found")
        else:
            for cred in creds:
                console.print(f'\nApplication     : [bold]{cred[0]}[/bold]')
                console.print(f'Username        : [bold]{cred[1]}[/bold]')
                console.print(f'Email/phone     : [bold]{cred[2]}[/bold]')
                password = self.decrypt(cred[3]).decode("utf-8")
                console.print(f'Password        : [bold]{password}[/bold]\n')
            if len(creds) == 1:
                copy(password)
            else:
                pass

    def main(self):
        menu()
        option = int(input("Choose one option from menu: "))
        if option == 1:
            app = str(Prompt.ask("Enter the name of the application")).strip()
            if app == "":
                console.print("Invalid Input")
            else:
                self.log_txt(app, x, __file__)
                self.fetch(app)
                self.log(app, x, __file__)
                pas = Prompt.ask("Do you need a new password", choices=["y", "n"], default="y")
                if pas == "y":
                    password = generate_password(20)
                    console.print(f"Your password is ready: [bold]{password}[/bold]")
                else:
                    pass
        elif option == 2:
            email = Prompt.ask("Enter email/phone you want to search")
            self.email_search(email)
        elif option == 3:
            app = str(Prompt.ask("Enter the name of the application")).strip()
            username = str(Prompt.ask("Enter the username of the application")).strip()
            email = str(Prompt.ask("Enter email/phone")).strip()
            val = str(Prompt.ask("Do you want to generate password", choices=["y", "n"], default="y"))
            if val == "y":
                password = generate_password(20)
            else:
                password = str(Prompt.ask("Enter password", password=True))
            self.add(app, username, email, password)
        elif option == 4:
            pass
        else:
            console.print("Enter a valide option")
            self.main()

if __name__ == "__main__":
    Main()

end = time.time()
print(f"Execution time: {end-start}")
time.sleep(3)
os.system("clear")
