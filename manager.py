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
        with open(os.path.join(self.home + "/.config/manager/config.py") , "w") as f:
            f.write(conf)
            f.close()
        backup(config.bak, os.path.join(self.home + "/.config/manager/config.py"), os.path.join(self.home + "/.config/manager/backup"))
        console.print("Please run the script again")
        quit(0)


