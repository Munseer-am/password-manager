import os
import logging
from config import Config
from lib import printTable, decrypt
from database import DataBase
from rich.table import Table
from rich.console import Console

console: Console = Console()

class Core:
    def __init__(self) -> None:
        self.config: Config = Config()
        self.base_dir: str = self.config.getPath("config_dir")
        self.logFile: str = self.config.getPath("logs_file")
        self.db: DataBase = DataBase(os.path.join(self.base_dir, "db.sqlite3")) 
        self.conf = self.config.readConfig()

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


