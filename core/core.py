import os
import json
import logging
from config import Config
from database import DataBase
from rich.table import Table
from rich.console import Console
from cryptography.fernet import Fernet
from lib import printTable, decrypt, ask, checkMatch, isValidEmail, encoder, backup

console: Console = Console()

class Core:
    def __init__(self) -> None:
        self.config: Config = Config()
        self.base_dir: str = self.config.getPath("config_dir")
        self.config_file: str = self.config.getPath("config")
        self.logFile: str = self.config.getPath("logs_file")
        self.backups: str = self.config.getPath("backups")
        self.db_path: str = os.path.join(self.base_dir, "db.sqlite3")
        self.db: DataBase = DataBase(self.db_path) 
        self.conf: dict = self.config.readConfig()

    def listApps(self) -> None:
        t: str = "Passwords"
        apps: list = self.db.fetch(t, "Application")
        if len(apps) <= 0:
            console.print("No apps found")
            return None
        table: Table = printTable("Apps", ["Application"], apps)
        console.print(table, justify="left")

    def emailSearch(self, email: str) -> None:
        t: str = "Passwords"
        apps: list = self.db.fetch(t, "Application", "Email", email)
        if len(apps) <= 0:
            console.print("No apps found")
            return None
        table: Table = printTable(f"Apps connected to {email}", ["Application"], apps)
        console.print(table, justify="left")

    def getCreds(self, app: str):
        t: str = "Passwords"
        apps: list = self.db.fetch(t, filter_obj="Application", filter_val=app, strict_filter=False)
        if len(apps) <= 0:
            console.print("[bold]Oops! looks like there are no results for you[/bold]")
            return None
        apps = [list(app) for app in apps]
        for app in apps:
            for a in app:
                try:
                    dec = decrypt(self.conf["ENCRYPTION_KEY"],a)
                    app.remove(a)
                    app.append(dec.decode())
                except Exception as e:
                    continue
        table: Table = printTable("Credentials", self.db.list_columns(t), apps)
        console.print(table, justify="left")

    def log(self, app: str, current_time: str, script: str):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        log_file = self.logFile
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info(f"Time: {current_time} Script: {script} Application: {app.title()}")
        self.db.insert("Log", (app, str(current_time), script))


    def setDetails(self):
        master: str = ask("Set A Master Password", password=True)
        val: str = ask("Enter Password Again", password=True)
        if not checkMatch(master, val):
            console.print("[bold]Password Does Not Match[/bold]")
            return None
        if len(master) < 6:
            console.print("[bold]Password Must Be Minimum 6 Characters Long[/bold]")
            return None
        email: str = ask("Enter Your Email Address")
        if not isValidEmail(email):
            console.print("[bold]Enter A Valid Email[/bold]")
            return None
        encEmail: str = encoder(email)
        encPass: str = encoder(master)
        key: bytes = Fernet.generate_key()
        self.config.storeToken(key)
        conf = {"KEY": encPass, "EMAIL": encEmail}
        with open(self.config_file, "w") as f:
            json.dump(conf, f, indent=4)
            f.close()
        backup(self.config_file, os.path.join(self.backups, "config.json.bak"))
        backup(self.db_path, os.path.join(self.backups, "db.sqlite3.bak"))
        console.print("Please re-run the script")
        quit()

    def resetPassword(self):
        email: str = ask("Enter email address")
        if not isValidEmail(email):
            console.print("[bold]Enter A Valid Email[/bold]")
            return None
        encEmail: str = encoder(email)
        if str(self.conf["EMAIL"]) != encEmail:
            console.print("Email Doesn't Match")
            return None
        master = ask("Set A Master Password", password=True)
        val = ask("Enter Password Again", password=True)
        if not checkMatch(master, val):
            console.print(console.print("[bold]Password Does Not Match[/bold]"))
            return None
        if len(master) < 6:
            console.print("[bold]Password Must Be Minimum 6 Characters Long[/bold]")
            return None
        self.conf['KEY'] = encoder(master)
        with open(self.config_file, "w") as f:
            json.dump(self.conf, f, indent=4)
            f.close()
        backup(self.config_file, os.path.join(self.backups, "config.json.bak"))
        backup(self.db_path, os.path.join(self.backups, "db.sqlite3.bak"))
        console.print("Password Reset Successful")
        quit()


core = Core()
core.resetPassword()
