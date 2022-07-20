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
    out = dec.decrypt(password)
    return out


def backup(db, path, dst):
    copyfile(path, f"{dst}/{db}")


class Main:
    def __init__(self):
        super(Main, self).__init__()
        self.home = os.path.expanduser("~")
        try:
            if sys.argv == "reset":
                pass
            else:
                self.security()
        except IndexError:
            self.conn = sqlite3.connect(f"{self.home}/.config/manager/db.sqlite3")
            self.cur = self.conn.cursor()
            if is_configured() != "NO":
                self.security()
            else:
                pass

    def main(self):
        pass

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
