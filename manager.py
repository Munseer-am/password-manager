#! /usr/bin/python
import time
from lib import *
from config import config
from threading import Thread
from rich.console import Console
from rich.prompt import Prompt

console = Console()
cmd("clear")

class main:
    def __init__(self):
        logo()
        self.key = key()
        console.print(date().replace(":", "[blink]:[/blink]"))
        self.security()

    def main(self):
        thread = Thread(target=capture, args=(config["PATH_TO_LOG"],))
        thread.daemon = True
        thread.start()
        app = str(Prompt.ask("\nEnter the name of the application")).strip()
        log_txt(config["PATH_TO_LOG"], app, __file__, date())
        creds(config["PATH_TO_DATABASE"], app)
        log(config["PATH_TO_DATABASE"], app, __file__, date())
        pas = str(Prompt.ask("\nDo you need a new password", choices=["y", "n"], default="y"))
        if pas in ("y"):
            console.print(generate_password(20))
        else:
            pass

    def security(self):
        i = 0
        inp = str(Prompt.ask("Enter the password to unlock file", password=True)).strip()
        enc = md5_encoder(inp)
        while self.key != enc:
            i += 1
            print("Invalid Password!")
            if i >= 3:
                break
            else:
                inp = str(Prompt.ask("\nTry again", password=True))
                enc = md5_encoder(inp)
        else:
            print("Access Granted!")
            self.main()

if __name__ == "__main__":
    main()

time.sleep(3)
cmd("clear")
