#! /usr/bin/env python
import os
import sqlite3
import random
import sys
import pyperclip
import time
import datetime
import hashlib
from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from string import *
from shutil import copyfile

sys.path.insert(0, f"{os.path.expanduser('~')}/.config/manager/")
from config import config
from menu import menu

start = time.time()
console = Console()
os.system("clear")
os.system("figlet -c -f Bloody 'Munseer' | lolcat")
x = str(datetime.datetime.now().strftime("%H:%M:%S %b %d %Y"))
console.print(x.replace(":", "[blink]:[/blink]"))


def generate_password():
    sym = ":;!@#$%^&*(){}[]~|"
    full = ascii_uppercase + ascii_lowercase + digits + sym
    r = random.sample(full, 20)
    password = "".join(r)
    return password


def md5_encoder(word):
    enc = hashlib.md5(word.encode("utf-8")).hexdigest()
    return enc


def copy(text):
    pyperclip.copy(text)
    pyperclip.paste()


def log_txt(app, current_time, script):
    with open(f"{config['PATH_TO_LOG']}/logs.log", "a") as f:
        f.write(f"\nTime: {current_time} Script: {script} Application: {app}")
        f.close()


def is_configured():
    if config is not None:
        return "OK"
    else:
        return "NO"


def encrypt(key, password: str):
    enc = Fernet(key)
    out = enc.encrypt(password.encode("utf-8"))
    return out


def decrypt(key, password: bytes):
    dec = Fernet(key)
    out = dec.decrypt(password).decode("utf-8")
    return out


def backup(db, path, dst):
    copyfile(path, f"{dst}/{db}")


class Main:
    def __init__(self):
        super(Main, self).__init__()
        self.home = os.path.expanduser("~")
        print(self.home)
        try:
            if sys.argv[1] == "reset":
                pass
            else:
                pass
        except IndexError:
            self.conn = sqlite3.connect(f"{self.home}/.config/manager/db.sqlite3")
            self.cur = self.conn.cursor()
            if is_configured() != "NO":
                self.security()
            else:
                pass

    def set_details(self):
        createTable = """CREATE TABLE IF NOT EXISTS Passwords (
            Application VARCHAR(100),
            Username VARCHAR(100),
            Email VARCHAR(100),
            Password VARCHAR(100)
        );"""
        createLog = """CREATE TABLE IF NOT EXISTS Log (
            App VARCHAR(100),
            Time VARCHAR(100),
            Script VARCHAR(100),
        );"""
        self.cur.execute(createTable)
        self.cur.execute(createLog)
        self.conn.commit()
        self.conn.close()
        master = Prompt.ask("Set a master password to use", password=True).strip()
        val = Prompt.ask("Enter password again", password=True)
        if master != val:
            console.print("Password does not match")
            self.set_details()
        email = Prompt.ask("Enter your email address")
        if "@" not in email:
            console.print("Please enter a valid email address")
            self.set_details()
        else:
            email = md5_encoder(email)
        key = Fernet.generate_key()
        enc = md5_encoder(master)
        with open(f"{self.home}/.config/manager/config.py", "w") as f:
            conf = f"""config = {{
    'KEY': '{enc}',
    'ENCRYPTION_KEY': {key},
    'EMAIL': '{email}',
    'PATH_TO_DATABASE': '{self.home}/.config/manager/db.sqlite3',
    'PATH_TO_BACKUP': '{self.home}/.config/manager/backup/',
    'PATH_TO_LOG': '{self.home}/.config/manager/log/'
}}"""
            f.write(conf)
            f.close()
            console.print("Please run the script again")
            quit()

    def main(self):
        menu()
        option = int(input("Choose one option from menu: "))
        if option == 1:
            app = str(Prompt.ask("\nEnter the name of the application")).strip()
            log_txt(app, x, __file__)
            self.fetch(app)
            self.log(app, x, __file__)
            pas = Prompt.ask("Do you need a new password", choices=["y", "n"], default="y")
            if pas == "y":
                password = generate_password()
                console.print(f"Your password is ready: [bold]{password}[/bold]")
                copy(password)
        elif option == 2:
            email = Prompt.ask("Enter the email/phone you want to search")
            self.email_search(email)
        elif option == 3:
            app = str(Prompt.ask("Enter the name of the application")).strip()
            username = str(Prompt.ask("Enter username of the application")).strip()
            email = str(Prompt.ask("Enter email address")).strip()
            pas = Prompt.ask("Do you want to generate new password", choices=["y", "n"], default="y")
            if pas == "y":
                password = generate_password()
            else:
                password = str(Prompt.ask("Enter password", password=True)).strip()
            self.add(app, username, email, encrypt(config["ENCRYPTION_KEY"], password))
            backup("backup.db", config["PATH_TO_DATABASE"], config["PATH_TO_BACKUP"])
        elif option == 4:
            pass
        else:
            console.print("Please choose valid option\n")
            self.main()

    def fetch(self, app):
        self.cur.execute(f"SELECT * FROM PASSWORDS WHERE APPLICATION LIKE '%{app}%'")
        credentials = self.cur.fetchall()
        table = Table(
            title="Credentials"
        )
        table.add_column("Application", style="cyan", no_wrap=True)
        table.add_column("Username", style="cyan", no_wrap=True)
        table.add_column("Email/Phone", style="cyan", no_wrap=True)
        table.add_column("Password", style="cyan", no_wrap=True)
        for credential in credentials:
            password = decrypt(config["ENCRYPTION_KEY"], credential[3])
            table.add_row(credential[0], credential[1], credential[2], password)
            if len(credentials) == 1:
                copy(password)
            else:
                pass
        console.print(table, justify="left")

    def add(self, app, username, email, password):
        inserter = f"""INSERT INTO PASSWORDS VALUES (?, ?, ?, ?)"""
        self.cur.execute(inserter, (app.title(), username, email, password))
        self.conn.commit()
        self.conn.close()

    def email_search(self, email):
        self.cur.execute(f'SELECT APPLICATION FROM PASSWORDS WHERE EMAIL LIKE "%{email}%"')
        emails = self.cur.fetchall()
        console.print(f"\nFound [blink]{len(emails)}[/blink] apps connected to this email\n")
        for email in emails:
            email = "".join(email)
            console.print(f"Application:  [bold]{email}[/bold]")

    def log(self, app, current_time, script):
        inserter = f"""INSERT INTO LOG VALUES (?, ?, ?)"""
        self.cur.execute(inserter, (str(app).capitalize(), current_time, script))
        self.conn.commit()
        self.conn.close()

    def security(self):
        inp = str(Prompt.ask("Enter password to unlock file", password=True)).strip()
        enc = md5_encoder(inp)
        i = 0
        while enc != config["KEY"]:
            print("Access Denied!")
            i += 1
            if i >= 3:
                break
            else:
                inp = str(Prompt.ask("\nTry again", password=True)).strip()
                enc = md5_encoder(inp)
        else:
            print("Access Granted!")
            self.main()


if __name__ == "__main__":
    Main()

end = time.time()
console.print(f"Execution time: {end - start}")
time.sleep(5)
os.system("clear")
