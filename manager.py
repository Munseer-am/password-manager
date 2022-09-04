#! /usr/bin/env python3
import argparse
import clipboard
import os
# import re
import sqlite3
import sys
from cryptography.fernet import Fernet
from functools import cache
from hashlib import sha256
from random import sample
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from shutil import copyfile
from string import ascii_lowercase, ascii_uppercase, digits

sys.path.insert(0, os.path.join(os.path.expanduser("~") + "/.config/manager/"))
from config import config
from menu import menu

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--reset", help="reset the password of script")
parser.add_argument("-U", "--uninstall", help="Delete script file from /usr/local/bin/")
args = parser.parse_args()

console = Console()


@cache
def generate_password():
    sym = "!@#$%^&*()[]{}:;"
    all_chars = ascii_uppercase + ascii_lowercase + sym + digits
    r = sample(all_chars, 20)
    return "".join(r)


@cache
def sha256_encoder(word: str):
    enc = sha256(word.encode("utf-8")).hexdigest()
    return enc


@cache
def copy(word: str):
    clipboard.copy(word)
    clipboard.paste()


@cache
def is_not_configured():
    if config is not None:
        return False
    else:
        return True


@cache
def uninstall_script():
    pas = Prompt.ask("Enter password to delete", password=True)
    hashed = sha256_encoder(pas)
    if hashed != config["KEY"]:
        console.print("Invalid Password")
    else:
        os.system("sudo rm /usr/local/bin/manager")


@cache
def encrypt(key: bytes, password: str):
    enc = Fernet(key)
    return enc.encrypt(password.encode("utf-8"))


@cache
def decrypt(key: bytes, password: bytes):
    dec = Fernet(key)
    return dec.decrypt(password).decode("utf-8")


@cache
def backup(db: str, path: str, dst: str):
    copyfile(path, os.path.join(dst + "/" + db))


class Main:
    def __init__(self):
        super(Main, self).__init__()
        self.home = os.path.expanduser("~")
        self.conn = sqlite3.connect(os.path.join(self.home + "/.config/manager/db.sqlite3"))
        self.cur = self.conn.cursor()
        if is_not_configured():
            self.set_details()
        else:
            if args.reset:
                self.reset()
            elif args.uninstall():
                uninstall_script()
            else:
                pass

    def set_details(self):
        tables = """CREATE TABLE IF NOT EXISTS Passwords (
            Application VARCHAR(200),
            Username VARCHAR(200),
            Email VARCHAR(200),
            Password VARCHAR(200)
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
        master = Prompt.ask("Set a master password to use", password=True)
        val = Prompt.ask("Enter password again", password=True)
        if master != val:
            console.print("[bold]Password does not match[/bold]")
            self.set_details()
        email = Prompt.ask("Enter your email address(It will be used to reset password)")
        if "@" not in email:
            console.print("Enter a valid email address")
            self.set_details()
        email = sha256_encoder(email)
        key = Fernet.generate_key()
        enc = sha256_encoder(master)
        conf = f"""{{
    'KEY': '{enc},
    'ENCRYPTION_KEY': '{key}',
    'EMAIL': '{email}',
    'PATH_TO_DATABASE': '{os.path.join(self.home + "/.config/manager/db.sqlite3")}',
    'PATH_TO_BACKUP': '{os.path.join(self.home + "/.config/manager/backup/")}',
    'PATH_TO_LOG': '{os.path.join(self.home + "/.config/manager/log/")}'            
}}"""
        with open(os.path.join(self.home + "/.config/manager/config.py"), "w") as f:
            f.write(conf)
            f.close()
        backup(config.bak, os.path.join(self.home + "/.config/manager/config.py"),
               os.path.join(self.home + "/.config/manager/backup"))
        console.print("Please run the script again")
        quit(0)

    def reset(self):
        email = Prompt.ask("Enter email address")
        if "@" not in email:
            console.print("Please Enter a valid email")
            self.reset()
        hashed = sha256_encoder(email)
        if hashed != config["EMAIL"]:
            console.print("Email does not match")
        else:
            master = Prompt.ask("Set a master password to use", password=True)
            val = Prompt.ask("Enter password again", password=True)
            if master != val:
                console.print("Password does not match")
            else:
                key = sha256_encoder(master)
                conf = f"""config = {{
    'KEY': '{key}',
    'ENCRYPTION_KEY': '{config["ENCRYPTION_KEY"]}',
    'EMAIL': '{config["EMAIL"]}',
    'PATH_TO_DATABASE: '{config["PATH_TO_DATABASE"]}',
    'PATH_TO_BACKUP': '{config["PATH_TO_BACKUP"]}',
    'PATH_TO_LOG': '{config["PATH_TO_LOG"]}'
}}"""
                with open(os.path.join(self.home + "/.config/manager/config.py"), "w") as f:
                    f.write(conf)
                    f.close()
                backup(config.bak, os.path.join(self.home + "/.config/manager/config.py"),
                       os.path.join(self.home + "/.config/manager/backup"))
                console.print("Password Changed Successfully")
                quit(0)

    def security(self):
        inp = Prompt.ask("Enter password to unlock file", password=True)
        enc = sha256_encoder(inp)
        i = 0
        while enc != config["KEY"]:
            console.print("Access Denied!")
            i += 1
            if i >= 3:
                break
            else:
                inp = Prompt.ask("\nTry again", password=True)
                enc = sha256_encoder(inp)

    def fetch(self, app: str):
        self.cur.execute(f"SELECT * FROM Passwords WHERE Application LIKE '%{app}%'")
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
            console.print(table, justify="center")
        else:
            console.print("[bold]Oops! looks like there are no results for you[/bold]")

    def email_search(self, email: str):
        self.cur.execute(f'SELECT APPLICATION FROM Passwords WHERE Email LIKE "%{email}%"')
        emails = self.cur.fetchall()
        console.print(f"\nFound [bold][blink]{len(emails)}[/blink][/bold] apps connected to this email\n")
        for email in emails:
            email = "".join(email)
            console.print(f"Application: [bold]{email}[/bold]")
