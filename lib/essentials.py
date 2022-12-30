#! /usr/bin/env python3
import datetime
import clipboard
import os
import sqlite3
import sys
from cryptography.fernet import Fernet
from functools import cache
from hashlib import sha256
from random import sample
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from shutil import copyfile, rmtree
from string import ascii_lowercase, ascii_uppercase, digits
from threading import Thread

__author__ = "Munseer-am"
__version__ = "1.0.1"

try:
    sys.path.insert(0, f"{os.path.expanduser('~')}/.config/manager")
    from config import config
    from menu import menu
    from insults import insult
except ImportError:
    os.system("sudo rm /usr/local/bin/manager")
    os.system("manager_repair")
    sys.exit(0)

console = Console()
x = str(datetime.datetime.now().strftime("%H:%M:%S %b %d %Y"))

@cache
def generate_password():
    sym = "!@#$%^&*()[]{}:;"
    all_chars = ascii_uppercase + ascii_lowercase + sym + digits
    password = "".join(random.sample(all_chars, 20))
    return password


def sha256_encoder(word: str):
    enc = sha256(word.encode("utf-8")).hexdigest()
    return enc


def copy(word: str):
    clipboard.copy(word)
    clipboard.paste()


@cache
def is_not_configured():
    if config is not None:
        return False
    else:
        return True


def uninstall_script():
    pas = Prompt.ask("Enter password to delete", password=True)
    hashed = sha256_encoder(pas)
    if hashed != config["KEY"]:
        console.print("Invalid Password")
    else:
        os.system("sudo rm /usr/local/bin/manager")


def encrypt(key: bytes, password: str):
    enc = Fernet(key)
    return enc.encrypt(password.encode("utf-8"))


def decrypt(key: bytes, password: bytes):
    dec = Fernet(key)
    return dec.decrypt(password).decode("utf-8")


def backup(db: str, path: str, dst: str):
    copyfile(path, os.path.join(dst + "/" + db))


class Main:
    def __init__(self):
        super(Main, self).__init__()
        self.home = os.path.expanduser("~")
        try:
            if os.path.exists(f"{self.home}/.config/manager/"):
                if os.path.exists(f"{self.home}/.config/manager/db.sqlite3"):
                    self.conn = sqlite3.connect(f"{self.home}/.config/manager/db.sqlite3")
                elif os.path.exists(f"{self.home}/.config/manager/backup/db.sqlite3.bak"):
                    self.conn = sqlite3.connect(f"{self.home}/.config/manager/backup/db.sqlite3.bak")
                else:
                    self.conn = sqlite3.connect(f"{self.home}/.config/manager/db.sqlite3")
                self.cur = self.conn.cursor()
                self.create_tables()
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            os.system("sudo rm /usr/local/bin/manager")
            os.system("manager_repair")

    def create_tables(self, status=False):
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
        if status:
            self.conn.close()

    def set_details(self):
        master = Prompt.ask("Set a master password to use", password=True)
        val = Prompt.ask("Enter password again", password=True)
        if len(master) != 6:
            console.print("[bold]Password Must Be Minimum 6 Characters Long[/bold]")
            self.set_details()
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
        conf = f"""# config file for manager used for many purpose
# editing it may break the program
# edit at your own risk\n
config = {{
    'KEY': '{enc}',
    'ENCRYPTION_KEY': {key},
    'EMAIL': '{email}',
    'PATH_TO_DATABASE': '{self.home}/.config/manager/db.sqlite3',
    'PATH_TO_BACKUP': '{self.home}/.config/manager/backup/',
    'PATH_TO_LOG': '{self.home}/.config/manager/log/'            
}}"""
        with open(f"{self.home}/.config/manager/config.py", "w") as f:
            f.write(conf)
            f.close()
        backup("config.bak", f"{self.home}/.config/manager/config.py",
               f"{self.home}/.config/manager/backup")
        console.print("Please run the script again")
        self.conn.commit()
        self.conn.close()
        copyfile(f"{self.home}/.config/manager/db.sqlite3", f"{self.home}/.config/manager/backup/db.sqlite3.bak")
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
            if len(master) <= 0:
                console.print("Invalid Input")
                self.reset()
            if master != val:
                console.print("Password does not match")
            else:
                key = sha256_encoder(master)
                conf = f"""# config file for manager used for many purpose
# editing it may break the program
# edit at your own risk\n
config = {{
    'KEY': '{key}',
    'ENCRYPTION_KEY': {config["ENCRYPTION_KEY"]},
    'EMAIL': '{config["EMAIL"]}',
    'PATH_TO_DATABASE': '{config["PATH_TO_DATABASE"]}',
    'PATH_TO_BACKUP': '{config["PATH_TO_BACKUP"]}',
    'PATH_TO_LOG': '{config["PATH_TO_LOG"]}'
}}"""
                with open(os.path.join(f"{self.home}/.config/manager/config.py"), "w") as f:
                    f.write(conf)
                    f.close()
                backup("config.bak", f"{self.home}/.config/manager/config.py",
                       f"{self.home}/.config/manager/backup")
                console.print("Password Changed Successfully")
                quit(0)

    def security(self):
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
            self.main()

    def log(self, app: str, current_time: str, script: str):
        with open(os.path.join(config["PATH_TO_LOG"] + "/logs.log"), "a") as f:
            f.write(f"\nTime: {current_time} Script: {script} Application: {app.title()}")
            f.close()
        inserter = f"""INSERT INTO Log VALUES (?, ?, ?)"""
        self.cur.execute(inserter, (app.title(), current_time, script))
        self.conn.commit()

    @cache
    def list_apps(self):
        self.cur.execute("SELECT Application FROM Passwords")
        _apps = self.cur.fetchall()
        if len(_apps) == 0:
            console.print("[bold]No apps found[/bold]")
        else:
            _table = Table()
            _table.add_column("Application", style="cyan", no_wrap=True)
            for _app in _apps:
                _table.add_row("".join(_app))
            console.print(_table, justify="left")

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
            console.print(table, justify="left")
        else:
            console.print("[bold]Oops! looks like there are no results for you[/bold]")

    def email_search(self, email: str):
        if email == "" or email == " ":
            console.print("[bold]Invalid Input[/bold]")
        else:
            self.cur.execute(f'SELECT APPLICATION FROM Passwords WHERE Email LIKE "%{email}%"')
            emails = self.cur.fetchall()
            console.print(f"\nFound [bold][blink]{len(emails)}[/blink][/bold] apps connected to this email")
            if len(emails) != 0:
                table = Table(title=f"Apps connected to {email}")
                table.add_column("Apps", style="cyan", no_wrap=True)
                for email in emails:
                    table.add_row(email[0])
                console.print(table)
            else:
                console.print("[bold]No apps found[/bold]")

    def delete(self):
        uninstall_script()
        if os.path.exists(f"{self.home}/.config/manager/"):
            rmtree(f"{self.home}/.config/manager/")
        if os.path.exists("/usr/local/bin/manager_repair"):
            os.system("sudo rm /usr/local/bin/manager_repair")

    def update_data(self, application: str, app: str, username: str, email, password: bytes):
        self.remove(application)
        self.add(app, username, email, password)

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
        if app == " " or app == "":
            console.print("Invalid Input")
        else:
            self.cur.execute(f'SELECT Application FROM Passwords WHERE Application="{app.capitalize()}"')
            _apps = self.cur.fetchall()
            if len(_apps) != 0:
                for _app in _apps:
                    _app = "".join(_app)
                    self.cur.execute(f'DELETE FROM Passwords WHERE Application LIKE "%{_app}%"')
                    self.conn.commit()
                return True
            else:
                console.print("no such app to delete".capitalize())

    @cache
    def main(self):
        menu()
        try:
            option = int(input("Choose one option: "))
            if option == 1:
                app = Prompt.ask("Enter the name of the application").strip()
                if app == "":
                    console.print("Invalid Input")
                else:
                    thread = Thread(target=self.log, args=(app, x, __file__,))
                    thread.daemon = True
                    thread.run()
                    self.fetch(app)
                    self.conn.close()
            elif option == 2:
                self.list_apps()
            elif option == 3:
                email = Prompt.ask("Enter the email/phone that you want to search").strip()
                self.email_search(email)
            elif option == 4:
                app = Prompt.ask("Enter the name of the application").strip()
                if app == "" or app == " ":
                    console.print("Invalid Input")
                else:
                    username = Prompt.ask("Enter username of the application").strip()
                    email = Prompt.ask("Enter your email address").strip()
                    pas = Prompt.ask("Do you want to generate new password", choices=["y", "n"], default="y").strip()
                    if pas == "y":
                        password = generate_password()
                        copy(password)
                    else:
                        password = Prompt.ask("Enter password", password=True).strip()
                    self.add(app, username, email, encrypt(config['ENCRYPTION_KEY'], password))
                    backup("backup.db", config["PATH_TO_DATABASE"], config["PATH_TO_BACKUP"])
            elif option == 5:
                application = Prompt.ask("Enter the application that you want to update").strip().title()
                self.cur.execute(f"SELECT * FROM Passwords WHERE Application='{application}'")
                _apps = self.cur.fetchone()
                if _apps is not None:
                    app = Prompt.ask(f"Enter name of app (leave blank to use {''.join(_apps[0])})").strip()
                    if app == "" or app == " ":
                        app = "".join(_apps[0])
                    username = Prompt.ask(f"Enter username (leave blank to use {''.join(_apps[1])})").strip()
                    if username == "" or username == " ":
                        username = "".join(_apps[1])
                    email = Prompt.ask(f"Enter email/phone (leave blank to use {''.join(_apps[2])})").strip()
                    if email == "" or email == " ":
                        email = "".join(_apps[2])
                    password = Prompt.ask("Enter password", password=True).strip()
                    self.update_data(application, app, username, email,
                                     encrypt(config["ENCRYPTION_KEY"], password))
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
            else:
                console.print("Please choose a valid option \n")
                self.main()
        except ValueError:
            console.print("Enter int instead of str ")
            self.main()
