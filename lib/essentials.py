#! /usr/bin/python3
import datetime
import clipboard
import json
import logging
import os
import re
import sqlite3
import sys
import time
from cryptography.fernet import Fernet
from functools import cache
from hashlib import sha256
from pathlib import Path
from random import sample
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from shutil import copyfile, rmtree
from string import ascii_lowercase, ascii_uppercase, digits
from threading import Thread

__author__ = "Munseer-am"

try:
    sys.path.insert(0, f"{os.path.expanduser('~')}/.config/manager")
    from menu import menu
    from insults import insult
except ImportError:
    os.system("sudo rm /usr/local/bin/manager")
    os.system("manager_repair")
    sys.exit(0)

console = Console()
x = str(datetime.datetime.now().strftime("%H:%M:%S %b %d %Y"))

home = os.path.expanduser("~")
encoding = "UTF-8"
config_file = f"{home}/.config/manager/config.json"

def transfer():
    def check(file: str):
        return os.path.exists(file)
    if check(f"{home}/.config/manager/config.py") and not check(config_file):
        try:
            from config import config
            password = config["ENCRYPTION_KEY"].decode(encoding)
            config["ENCRYPTION_KEY"] = password
            with open(config_file, "w") as e:
                json.dump(config, e, indent=4)
                e.close()
            print("Configuration Tranfer Completed! run the script again")
            exit()
        except:
            raise Exception
            

@cache
def read_config():
    try:
        with open(config_file) as f:
            config = json.load(f)
            f.close()
        password = config["ENCRYPTION_KEY"]
        config["ENCRYPTION_KEY"] = password.encode(encoding)
        return config
    except FileNotFoundError:
        print("FileNotFoundError")
        transfer()
    except json.decoder.JSONDecodeError:
        print("DEcode Error")
        return None

@cache
def generate_password():
    sym = "!@#$%^&*()[]{}:;"
    all_chars = ascii_uppercase + ascii_lowercase + sym + digits
    password = "".join(sample(all_chars, 20))
    return password

config = read_config()

def sub_print(text, leading_spaces=0):
    text_chars = list(text)
    current, mutated = "", ""
    for i in range(len(text)):
        original = text_chars[i]
        current += original
        mutated += f"\033[1;38;5;82m{text_chars[i].upper()}\033[0m"
        print(f'\r{" " * leading_spaces}{mutated}', end="")
        time.sleep(0.05)
        print(f'\r{" " * leading_spaces}{current}', end="")
        mutated = current

    print(f'\r{" " * leading_spaces}{text}\n')


def sha256_encoder(word: str):
    enc = sha256(word.encode(encoding)).hexdigest()
    return enc


def copy(word: str):
    clipboard.copy(word)
    clipboard.paste()


@cache
def is_not_configured():
    if read_config() is not None:
        return False
    else:
        return True


def uninstall_script():
    if os.path.exists("/usr/local/bin/manager"):
        os.system("sudo rm /usr/local/bin/manager")
    else:
        console.print("File does not exist")


def encrypt(key: bytes, password: str):
    enc = Fernet(key)
    return enc.encrypt(password.encode(encoding))


def decrypt(key: bytes, password: bytes):
    dec = Fernet(key)
    return dec.decrypt(password).decode(encoding)


def backup(db: str, path: str, dst: str):
    copyfile(path, os.path.join(dst + "/" + db))


def is_valid_email(email):
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(regex, email):
        return True
    else:
        return False


class Main:
    def __init__(self):
        super(Main, self).__init__()
        self.db_paths = [
            f"{home}/.config/manager/db.sqlite3",
            f"{home}/.config/manager/backup/db.sqlite3.bak",
        ]
        try:
            for path in self.db_paths:
                if os.path.exists(path):
                    self.conn = sqlite3.connect(path)
                    break
            else:
                self.conn = sqlite3.connect(self.db_paths[0])
            self.cur = self.conn.cursor()
            self.create_tables()
        except FileNotFoundError:
            os.system("manager_repair")

    def create_tables(self):
        tables = """CREATE TABLE IF NOT EXISTS Passwords (
            Application VARCHAR(200),
            Username VARCHAR(200),
            Email VARCHAR(200),
            Password BLOB
        );"""
        log = """CREATE TABLE IF NOT EXISTS Log (
            App VARCHAR(100),
            Time VARCHAR(100),
            Script VARCHAR(100)
        );"""
        self.cur.execute(tables)
        self.cur.execute(log)
        self.conn.commit()

    def set_details(self):
        master = Prompt.ask("Set a master password to use", password=True)
        val = Prompt.ask("Enter password again", password=True)
        if len(master) < 6:
            console.print("[bold]Password Must Be Minimum 6 Characters Long[/bold]")
            self.set_details()
        if master != val:
            console.print("[bold]Password does not match[/bold]")
            self.set_details()
        email = Prompt.ask(
            "Enter your email address(It will be used to reset password)"
        )
        if not is_valid_email(email):
            console.print("Enter a valid email address")
            self.set_details()
        email = sha256_encoder(email)
        key = Fernet.generate_key().decode(encoding)
        enc = sha256_encoder(master)
        conf = {
    'KEY': enc,
    'ENCRYPTION_KEY': key,
    'EMAIL': email,
    'PATH_TO_DATABASE': f'{home}/.config/manager/db.sqlite3',
    'PATH_TO_BACKUP': f'{home}/.config/manager/backup/',
    'PATH_TO_LOG': f'{home}/.config/manager/log/'            
}
        with open(f"{home}/.config/manager/config.json", "w") as f:
            json.dump(conf, f, indent=4)
            f.close()
        backup(
            "config.json.bak",
            f"{home}/.config/manager/config.json",
            f"{home}/.config/manager/backup",
        )
        console.print("Please run the script again")
        self.conn.commit()
        self.conn.close()
        copyfile(
            f"{home}/.config/manager/db.sqlite3",
            f"{home}/.config/manager/backup/db.sqlite3.bak",
        )

    def reset(self):
        email = Prompt.ask("Enter email address")
        if not is_valid_email(email):
            console.print("Please Enter a valid email")
            self.reset()
        hashed = sha256_encoder(email)
        if hashed != config["EMAIL"]:
            console.print("Email does not match")
        else:
            master = Prompt.ask("Set a master password to use", password=True)
            val = Prompt.ask("Enter password again", password=True)
            if len(master) <= 0:
                console.print("Invalid Input")
                self.reset()
            if master != val:
                console.print("Password does not match")
            else:
                key = sha256_encoder(master)
                conf = {
    'KEY': key,
    'ENCRYPTION_KEY': config["ENCRYPTION_KEY"],
    'EMAIL': config["EMAIL"],
    'PATH_TO_DATABASE': config["PATH_TO_DATABASE"],
    'PATH_TO_BACKUP': config["PATH_TO_BACKUP"],
    'PATH_TO_LOG': config["PATH_TO_LOG"]
}
                with open(
                    os.path.join(f"{home}/.config/manager/config.py"), "w"
                ) as f:
                    f.write(conf)
                    f.close()
                backup(
                    "config.bak",
                    f"{home}/.config/manager/config.py",
                    f"{home}/.config/manager/backup",
                )
                console.print("Password Changed Successfully")
                quit(0)

    def security(self, func):
        inp = Prompt.ask("Enter password to unlock file", password=True)
        enc = sha256_encoder(inp)
        i = 0
        while enc != config["KEY"]:
            i += 1
            if i >= 3:
                console.print("Access Denied!")
                break
            else:
                console.print(insult())
                inp = Prompt.ask("\nTry again", password=True)
                enc = sha256_encoder(inp)
        else:
            console.print("Access Granted!")
            func()

    def log(self, app: str, current_time: str, script: str):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        log_file = os.path.join(config["PATH_TO_LOG"] + "/logs.log")
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info(f"Time: {current_time} Script: {script} Application: {app.title()}")
        inserter = f"""INSERT INTO Log VALUES (?, ?, ?)"""
        self.cur.execute(inserter, (app.title(), current_time, script))
        self.conn.commit()

    @cache
    def list_apps(self):
        self.cur.execute("SELECT Application FROM Passwords")
        apps = self.cur.fetchall()
        if not apps:
            console.print("[bold]No apps found[/bold]")
        else:
            table = Table()
            table.add_column("Application", style="cyan", no_wrap=True)
            for app in apps:
                table.add_row(app[0])
            console.print(table, justify="left")

    def fetch(self, app: str):
        try:
            self.cur.execute(
                "SELECT * FROM Passwords WHERE Application LIKE ?", ("%" + app + "%",)
            )
            credentials = self.cur.fetchall()
            if len(credentials) != 0:
                table = Table(title="Credentials")
                table.add_column("Application", style="cyan", no_wrap=True)
                table.add_column("Username", style="cyan", no_wrap=True)
                table.add_column("Email/Phone", style="cyan", no_wrap=True)
                table.add_column("Password", style="cyan", no_wrap=True)
                for credential in credentials:
                    password = decrypt(config["ENCRYPTION_KEY"], credential[3])
                    table.add_row(credential[0], credential[1], credential[2], password)
                    if len(credentials) == 1:
                        copy(password)
                console.print(table, justify="left")
            else:
                console.print(
                    "[bold]Oops! looks like there are no results for you[/bold]"
                )
        except sqlite3.Error as e:
            console.print(f"An error occurred: {e}")
        finally:
            self.cur.close()
            self.conn.close()

    def email_search(self, email: str):
        if not email.strip():
            console.print("[bold]Invalid Input[/bold]")
        else:
            self.cur.execute(
                f'SELECT APPLICATION FROM Passwords WHERE Email LIKE "%{email}%"'
            )
            emails = self.cur.fetchone()
            count = 0
            table = Table(title=f"Apps connected to {email}")
            table.add_column("No", style="cyan", no_wrap=True)
            table.add_column("Apps", style="cyan", no_wrap=True)
            while emails:
                count += 1
                table.add_row(str(count), emails[0])
                emails = self.cur.fetchone()
            console.print(
                f"\nFound [bold][blink]{count}[/blink][/bold] apps connected to this email"
            )
            if count != 0:
                console.print(table)
            else:
                console.print("[bold]No apps found[/bold]")

    def delete(self):
        uninstall_script()
        try:
            if os.path.exists(f"{home}/.config/manager/"):
                rmtree(f"{home}/.config/manager/")
        except PermissionError:
            if os.path.exists("/usr/local/bin/manager_repair"):
                os.system("sudo rm /usr/local/bin/manager_repair")

    def update_data(
        self, application: str, app: str, username: str, email, password: bytes
    ):
        sql = "UPDATE Passwords SET Application=?, Username=?, Email=?, Password=? WHERE Application=?"
        self.cur.execute(sql, (app, username, email, password, application))
        self.conn.commit()
        self.conn.close()

    def add(self, app: str, username: str, email, password: str):
        inserter = f"""INSERT INTO Passwords VALUES(?, ?, ?, ?)"""
        self.cur.execute(inserter, (app.title(), username, email, password))
        self.conn.commit()
        self.conn.close()

    @cache
    def view_log(self):
        self.cur.execute("SELECT * FROM LOG")
        logs = self.cur.fetchall()
        if len(logs) != 0:
            _table = Table(title="Logs")
            _table.add_column("Received Input", style="cyan", no_wrap=False)
            _table.add_column("Date and Time", style="cyan", no_wrap=False)
            _table.add_column("Script Location", style="cyan", no_wrap=False)
            for _log in logs:
                _table.add_row(_log[0], _log[1], _log[2])
            console.print(_table)
            self.conn.close()

    def remove(self, app: str):
        if not app.strip():
            console.print("Invalid Input")
        else:
            self.cur.execute(
                f'SELECT Application FROM Passwords WHERE Application="{app.capitalize()}"'
            )
            _apps = self.cur.fetchall()
            if len(_apps) != 0:
                for _app in _apps:
                    _app = "".join(_app)
                    self.cur.execute(
                        f'DELETE FROM Passwords WHERE Application LIKE "%{_app}%"'
                    )
                    self.conn.commit()
                return True
            else:
                console.print("no such app to delete".capitalize())

    def main(self):
        menu()
        try:
            option = int(input("Choose one option: "))
            if option == 1:
                app = Prompt.ask("Enter the name of the application").strip()
                if not app.strip():
                    console.print("Invalid Input")
                else:
                    thread = Thread(
                        target=self.log,
                        args=(
                            app,
                            x,
                            __file__,
                        ),
                    )
                    thread.daemon = True
                    thread.run()
                    self.fetch(app)
                    self.conn.close()
            elif option == 2:
                self.list_apps()
            elif option == 3:
                email = Prompt.ask(
                    "Enter the email/phone that you want to search"
                ).strip()
                self.email_search(email)
            elif option == 4:
                app = Prompt.ask("Enter the name of the application").strip()
                if not app.strip():
                    console.print("Invalid Input")
                else:
                    username = Prompt.ask("Enter username of the application").strip()
                    email = Prompt.ask("Enter your email address").strip()
                    pas = Prompt.ask(
                        "Do you want to generate new password",
                        choices=["y", "n"],
                        default="y",
                    ).strip()
                    if pas == "y":
                        password = generate_password()
                        copy(password)
                    else:
                        password = Prompt.ask("Enter password", password=True).strip()
                    self.add(
                        app,
                        username,
                        email,
                        encrypt(config["ENCRYPTION_KEY"], password),
                    )
                    backup(
                        "db.sqlite3.bak",
                        config["PATH_TO_DATABASE"],
                        config["PATH_TO_BACKUP"],
                    )
            elif option == 5:
                application = (
                    Prompt.ask("Enter the application that you want to update")
                    .strip()
                    .title()
                )
                self.cur.execute(
                    f"SELECT * FROM Passwords WHERE Application='{application}'"
                )
                _apps = self.cur.fetchone()
                if _apps is not None:
                    app = Prompt.ask(
                        f"Enter name of app (leave blank to use {''.join(_apps[0])})"
                    ).strip()
                    if not app.strip():
                        app = "".join(_apps[0])
                    username = Prompt.ask(
                        f"Enter username (leave blank to use {''.join(_apps[1])})"
                    ).strip()
                    if not username.strip():
                        username = "".join(_apps[1])
                    email = Prompt.ask(
                        f"Enter email/phone (leave blank to use {''.join(_apps[2])})"
                    ).strip()
                    if not email.strip():
                        email = "".join(_apps[2])
                    password = Prompt.ask("Enter password", password=True).strip()
                    self.update_data(
                        application,
                        app,
                        username,
                        email,
                        encrypt(config["ENCRYPTION_KEY"], password),
                    )
                    console.print("Data updated successfully")
                else:
                    console.print("[bold]No such app to update[/bold]")
            elif option == 6:
                app = Prompt.ask("Enter the name of the app that you want to delete")
                if self.remove(app):
                    console.print(f"[bold]Deleted {app.title()} successfully[/bold]")
            elif option == 7:
                password = generate_password()
                copy(password)
                console.print(f"Your password is ready: [bold]{password}[/bold]")
            elif option == 8:
                self.view_log()
            elif option == 9:
                exit()
            else:
                console.print("Please choose a valid option \n")
                self.main()
        except ValueError:
            console.print("Enter int instead of str ")
            self.main()
