#! /usr/bin/env python
import argparse
import pyfiglet
import os
import json
import datetime
import time
import sys
from rich.console import Console

try:
    sys.path.insert(0, f"{os.path.expanduser('~')}/.config/manager/")
    from essentials import Main, is_not_configured, uninstall_script, decrypt, config
except ImportError:
    os.system("sudo rm /usr/local/bin/manager")
    os.system("manager_repair")
    exit()

console = Console()
console.clear()
os.system("figlet -c -f Bloody 'Manager' | lolcat")
x = str(datetime.datetime.now().strftime("%H:%M:%S %b %d %Y"))
console.print(x.replace(":", "[blink]:[/blink]"))

parse = argparse.ArgumentParser()
parser = parse.add_mutually_exclusive_group()
parser.add_argument("-r", "--reset", help="reset the password of script", action="store_true")
parser.add_argument("-U", "--uninstall", help="Delete script file from /usr/local/bin/", action="store_true")
parser.add_argument("--REMOVE", help="Delete all files and directories related to password manager",
                    action="store_true")
parser.add_argument("--dump-credentials", help="Dump all credentials into a json file", action="store_true")
args = parse.parse_args()

start = time.time()


class Main(Main):
    def __init__(self):
        super(Main, self).__init__()
        configured = not is_not_configured()
        if configured:
            options = {
                "reset": self.reset,
                "REMOVE": self.delete,
                "uninstall": uninstall_script,
                "dump_credentials": self.dump
            }
            for key, value in options.items():
                if getattr(args, key):
                    if key == "reset":
                        value()
                        break
                    else:
                        self.security(value)
                        break
            else:
                self.security(self.main)
        else:
            self.set_details()

    def dump(self):
        credentials = {}
        self.cur.execute("SELECT * FROM Passwords")
        creds = self.cur.fetchall()
        creds.sort()
        for cred in creds:
            credentials[cred[0]] = {}
            credentials[cred[0]]["Application"] = cred[0]
            credentials[cred[0]]["Username"] = cred[1]
            credentials[cred[0]]["Email/Phone"] = cred[2]
            credentials[cred[0]]["Password"] = decrypt(config["ENCRYPTION_KEY"], cred[3])

        with open("dump.json", "w") as f:
            f.write(json.dumps(credentials, indent=4))
            f.close()
        print(f"Data saved to file: dump.json")

try:
    if __name__ == "__main__":
        Main()
    end = time.time()
    print(f"Execution Time: {end-start}")
    time.sleep(4)
    console.clear()
except KeyboardInterrupt:
    console.clear()
    exit(0)
