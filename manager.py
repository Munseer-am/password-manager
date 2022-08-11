#! /usr/bin/env python
import argparse
import datetime
import hashlib
import os
import platform
import pyperclip
import random
import sqlite3
import sys
import time
from shutil import copyfile
from string import *
from shutil import which
from cryptography.fernet import Fernet
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

sys.path.insert(0, f"{os.path.expanduser('~')}/.config/manager/")
from config import config
from menu import menu

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--reset", help="Reset password of script", action="store_true")
parser.add_argument("-U", "--uninstall", help="Uninstall script from your machine", action="store_true")
args = parser.parse_args()

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


def sha256_encoder(word: str):
    enc = hashlib.sha256(word.encode("utf-8")).hexdigest()
    return enc


def copy(text: str):
    pyperclip.copy(text)
    pyperclip.paste()


def log_txt(app: str, current_time: str, script: str):
    with open(f"{config['PATH_TO_LOG']}/logs.log", "a") as f:
        f.write(f"\nTime: {current_time} Script: {script} Application: {app}")
        f.close()

def uninstall():
    os.system("sudo rm /usr/local/bin/manager")

def is_configured():
    if config is not None:
        return "OK"
    else:
        return "NO"


def encrypt(key: bytes, password: str):
    enc = Fernet(key)
    out = enc.encrypt(password.encode("utf-8"))
    return out


def decrypt(key: bytes, password: bytes):
    dec = Fernet(key)
    out = dec.decrypt(password).decode("utf-8")
    return out


def backup(db: str, path: str, dst: str):
    copyfile(path, f"{dst}/{db}")


def tool(tools: str):
    if which(tools) is None:
        return None
    else:
        return "INSTALLED"


class Main:
    def __init__(self):
        super(Main, self).__init__()
        self.home = os.path.expanduser("~")
        self.conn = sqlite3.connect(f"{self.home}/.config/manager/db.sqlite3")
        self.cur = self.conn.cursor()
        if is_configured() != "OK":
            self.set_details()
        else:
            if args.reset:
                self.reset()
            elif args.uninstall:
                uninstall()
            else:
                self.security()

    def reset(self):
        email = Prompt.ask("Enter your email address")
        if "@" not in email:
            console.print("Enter a valid email address")
            self.reset()
        else:
            enc = sha256_encoder(email)
            if enc != config["EMAIL"]:
                console.print("Email does not match")
            else:
                master = Prompt.ask("Set a master password to use", password=True)
                val = Prompt.ask("Enter password again", password=True)
                if master != val:
                    console.print("Password does not match")
                    self.reset()
                else:
                    key = sha256_encoder(master)
                    with open(f"{self.home}/.config/manager/config.py", "w") as f:
                        conf = f"""config = {{
    'KEY': '{key}',
    'ENCRYPTION_KEY': {config["ENCRYPTION_KEY"]},
    'EMAIL': '{config["EMAIL"]}',
    'PATH_TO_DATABASE': '{self.home}/.config/manager/db.sqlite3',
    'PATH_TO_BACKUP': '{self.home}/.config/manager/backup/',
    'PATH_TO_LOG': '{self.home}/.config/manager/log/'
}}"""
                        f.write(conf)
                        f.close()
                    console.print("Password changed successfully")
                    quit(0)

    def set_details(self):
        tables = """CREATE TABLE IF NOT EXISTS Passwords (
            Application VARCHAR(100),
            Username VARCHAR(100),
            Email VARCHAR(100),
            Password VARCHAR(100)
        );"""
        log = """CREATE TABLE IF NOT EXISTS Log (
            App VARCHAR(100),
            Time VARCHAR(100),
            Script VARCHAR(100)
        );"""
        self.cur.execute(tables)
        self.cur.execute(log)
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
            email = sha256_encoder(email)
        key = Fernet.generate_key()
        enc = sha256_encoder(master)
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
            backup("config.bak", f"{self.home}/.config/manager/config.py", f"{self.home}/.config/manager/backup/")
            console.print("Please run the script again")
            quit()

    def main(self):
        menu()
        option = int(input("Choose one option from menu: "))
        if option == 1:
            app = Prompt.ask("\nEnter the name of the application").strip()
            if app == "":
                console.print("Invalid Input")
                pass
            else:
                log_txt(app, x, __file__)
                self.fetch(app)
                self.log(app, x, __file__)
                pas = Prompt.ask("Do you need a new password", choices=["y", "n"], default="y")
                if pas == "y":
                    password = generate_password()
                    console.print(f"Your password is ready: [bold]{password}[/bold]")
                    # copy(password)
        elif option == 2:
            email = Prompt.ask("Enter the email/phone you want to search")
            self.email_search(email)
        elif option == 3:
            app = Prompt.ask("Enter the name of the application").strip()
            username = Prompt.ask("Enter username of the application").strip()
            email = Prompt.ask("Enter email address").strip()
            pas = Prompt.ask("Do you want to generate new password", choices=["y", "n"], default="y")
            if pas == "y":
                password = generate_password()
            else:
                password = Prompt.ask("Enter password", password=True).strip()
            self.add(app, username, email, encrypt(config["ENCRYPTION_KEY"], password))
            backup("backup.db", config["PATH_TO_DATABASE"], config["PATH_TO_BACKUP"])
        elif option == 4:
            pass
        else:
            console.print("Please choose valid option\n")
            self.main()

    def fetch(self, app: str):
        self.cur.execute(f"SELECT * FROM PASSWORDS WHERE APPLICATION LIKE '%{app}%'")
        credentials = self.cur.fetchall()
        if len(credentials) != 0:
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
        else:
            console.print("[bold]Oops! looks there's no result for you[/bold]")

    def add(self, app, username, email, password):
        inserter = f"""INSERT INTO PASSWORDS VALUES (?, ?, ?, ?)"""
        self.cur.execute(inserter, (app.title(), username, email, password))
        self.conn.commit()
        self.conn.close()

    def email_search(self, email: str):
        self.cur.execute(f'SELECT APPLICATION FROM PASSWORDS WHERE EMAIL LIKE "%{email}%"')
        emails = self.cur.fetchall()
        console.print(f"\nFound [blink]{len(emails)}[/blink] apps connected to this email\n")
        for email in emails:
            email = "".join(email)
            console.print(f"Application:  [bold]{email}[/bold]")

    def log(self, app, current_time, script):
        inserter = f"""INSERT INTO LOG VALUES (?, ?, ?)"""
        self.cur.execute(inserter, (str(app).title(), current_time, script))
        self.conn.commit()
        self.conn.close()

    def security(self):
        inp = Prompt.ask("Enter password to unlock file", password=True).strip()
        enc = sha256_encoder(inp)
        i = 0
        while enc != config["KEY"]:
            print("Access Denied!")
            i += 1
            if i >= 3:
                break
            else:
                inp = Prompt.ask("\nTry again", password=True).strip()
                enc = sha256_encoder(inp)
        else:
            print("Access Granted!")
            self.main()


if __name__ == "__main__":
    Main()

end = time.time()
console.print(f"Execution time: {end - start}")
time.sleep(5)
os.system("clear")
