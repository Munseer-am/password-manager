#! /usr/bin/env python3
import time
import argparse
import config
import threading
from getpass import getpass
from lib import *
from rich.traceback import install
from rich.console import Console
from rich.prompt import Prompt

start = time.time()

cmd("clear")

install(show_locals=True)
console = Console()

parser = argparse.ArgumentParser()
parser.add_argument(
        "-new", help="Enter Keyword to unlock database inserting", type=str)
parser.add_argument(
        "-a", help="Enter the name of the application", type=str)
parser.add_argument(
        "-u", help="Enter the username of the application", type=str)
parser.add_argument(
        "-e", help="Enter Email/phone of the application", type=str)
parser.add_argument(
        "-p", help="Enter the password of application", type=str)

args = parser.parse_args()

console.print(f"[bold][blue]{logo()} [/bold][/blue]")
date = date()
console.print(date.replace(":", "[blink]:[/blink]"))

class Main:
    def __init__(self):
        super().__init__()
        self.key = key(config.PATH_TO_DATABASE)
        if args.new:
            insert(config.PATH_TO_DATABASE, args.a, args.u, args.e, args.p)
        else:
            self.security()

    def main(self):
        thread = threading.Thread(target=capture, args=(config.PATH_TO_LOG,))
        thread.daemon = True
        thread.start()
        app = Prompt.ask("\nEnter the name of the application").strip()
        log_txt(config.PATH_TO_LOG, app, __file__ , date)
        creds(config.PATH_TO_DATABASE, app)
        log(config.PATH_TO_DATABASE, app, __file__, date)
        pas = Prompt.ask("\nDo you need a new password", choices=["y","n"], default="y").strip().lower()
        if pas in ("y"):
            password = generate_password(20)
            console.print(password)
        else:
            pass

    def security(self):
        try:
            i = 0
            inp = str(getpass("Enter password to unlock file: ")).strip()
            hash = md5_encoder(inp)
            while self.key != hash:
                print("Access Denied!")
                i += 1
                if i >= 3:
                    break
                else:
                    inp = str(getpass("\nTry again: ")).strip()
                    hash = md5_encoder(inp)
            else:
                print("Access Granted!")
                self.main()
        except Exception:
            console.print_exception(show_locals=True)

if __name__ == '__main__':
    Main()

end = time.time()
console.print(f"Execution Time: {end-start}")
time.sleep(3)
cmd("clear")
