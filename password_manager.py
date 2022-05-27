import argparse
import cv2
import datetime
import hashlib
import os
import random
import sqlite3
import threading
import time
from curses import KEY_NEXT
from getpass import getpass
from string import *

start = time.time()

os.system("clear")

print(""" __  __                                
|  \/  |_   _ _ __  ___  ___  ___ _ __ 
| |\/| | | | | '_ \/ __|/ _ \/ _ \ '__|
| |  | | |_| | | | \__ \  __/  __/ |   
|_|  |_|\__,_|_| |_|___/\___|\___|_|  """)

x = datetime.datetime.now().strftime("%H:%M:%S %b %d %Y")
print(x)
j = str(datetime.datetime.now())
j.replace(":", "-")

parser = argparse.ArgumentParser()
parser.add_argument("-new", help="Enter Keyword to unlock database inserting", type=str)
parser.add_argument("-a", help="Enter the name of the application", type=str)
parser.add_argument("-u", help="Enter the username of the application", type=str)
parser.add_argument("-e", help="Enter Email/phone of the application", type=str)
parser.add_argument("-p", help="Enter the password of application", type=str)

args = parser.parse_args()


def gen():
    low = ascii_lowercase
    up = ascii_uppercase
    num = digits
    sym = ';/#$%&^*(){}[]|'
    all = low + up + num + sym
    length = 20
    r = random.sample(all, length)
    password = "".join(r)
    print(f"Your password is ready: {password}")


def capture():
    cam = cv2.VideoCapture(0)
    result, img = cam.read()
    time.sleep(2)
    path = "/home/munseer/python/Log"
    cv2.imwrite(os.path.join(path, f"{j}.jpg"), img)
    cam.release()
    cv2.destroyAllWindows()


class Main:
    def insert(self, app, user, email, password):
        try:
            cur = self.pass_con.cursor()
            createTable = f"""CREATE TABLE IF NOT EXISTS {app} (
                Application VARCHAR(200),
                Username VARCHAR(200),
                Email VARCHAR(200),
                Password VARCHAR(200)
            );"""
            cur.execute(createTable)
            insertQuery = f"""INSERT INTO {app} VALUES (?, ?, ?, ?)"""
            cur.execute(insertQuery, (app, user, email, password))
            self.pass_con.commit()
            self.pass_con.close()
        except:
            print("Oops Something Went Wrong")

    def __init__(self):
        super().__init__()
        path = "/home/munseer/database"
        self.pass_con = sqlite3.connect(f"{path}/pass.db")
        key_con = sqlite3.connect(f"{path}/key.db")
        self.log_con = sqlite3.connect(f"{path}/log.db")
        cur = key_con.cursor()
        cur.execute("SELECT * FROM KEY")
        keys = cur.fetchall()
        for key in keys:
            self.key = "".join(key)

        if args.new in ("insert", "new"):
            self.insert(str(args.a).capitalize(), args.u, args.e, args.p)
        else:
            self.security()

    def creds(self, app):
        try:
            cur = self.pass_con.cursor()
            cur.execute(f"SELECT APPLICATION FROM {app}")
            creds = cur.fetchall()
            for cred in creds:
                application = "".join(cred)

            cur.execute(f"SELECT USERNAME FROM {app}")
            creds = cur.fetchall()
            for cred in creds:
                name = "".join(cred)

            cur.execute(f"SELECT EMAIL FROM {app}")
            creds = cur.fetchall()
            for cred in creds:
                mail = "".join(cred)

            cur.execute(f"SELECT PASSWORD FROM {app}")
            creds = cur.fetchall()
            for cred in creds:
                password = "".join(cred)

            print(f'\nApplication     : {application}')
            print(f'Username        : {name}')
            print(f'Email/phone     : {mail}')
            print(f'Password        : {password}')
        except sqlite3.Error:
            print("Invalid Input")

    def main(self):
        thread = threading.Thread(target=capture)
        thread.daemon = True
        thread.start()
        app = str(input("\nEnter The Name Of The Application: ")).strip().lower()
        with open("Log/logs.log", "a") as f:
            f.write(
                f"\nTime: {x} Script: {__file__} Application: {app.capitalize()}")
            f.close()
        self.creds(app)
        pas = str(input("\nDo you need a new password(y/n): ")).strip().lower()
        if pas in ('y', "yes"):
            gen()
        else:
            pass

        cur = self.log_con.cursor()
        insertQuery = f"""INSERT INTO LOG VALUES (?, ?, ?)"""
        cur.execute(insertQuery, (app.capitalize(), x, __file__))
        self.log_con.commit()
        self.log_con.close()

    def hash(self, word):
        enc = hashlib.md5(word.encode()).hexdigest()
        return enc

    def security(self):
        inp = str(getpass("\nEnter Password To Unlock File: ")).strip().lower()
        hash = self.hash(inp)
        i = 0
        while hash != self.key:
            i += 1
            if i >= 3:
                break
            else:
                inp = getpass("\nTry Again: ").strip().lower()
                hash = self.hash(inp)
        else:
            self.main()

if __name__ == "__main__":
    Main()

end = time.time()

print(f"Execution Time: {end-start}")
time.sleep(3)
os.system("clear")
