import hashlib
import cv2
import os
import sqlite3
import random
import time
import datetime
import subprocess
from playsound import playsound
from rich.console import Console
from string import *

console = Console()

def md5_encoder(word):
    enc = hashlib.md5(word.encode()).hexdigest()
    return enc


def logo():
    logo = """ __  __                                
|  \/  |_   _ _ __  ___  ___  ___ _ __ 
| |\/| | | | | '_ \/ __|/ _ \/ _ \ '__|
| |  | | |_| | | | \__ \  __/  __/ |   
|_|  |_|\__,_|_| |_|___/\___|\___|_|  """
    return logo


def capture(path_to_log_dir):
    j = str(datetime.datetime.now())
    j.replace(":", "-")
    cam = cv2.VideoCapture(0)
    result, img = cam.read()
    time.sleep(2)   
    cv2.imwrite(os.path.join(path_to_log_dir, f"{j}.jpg"), img)
    cam.release()
    cv2.destroyAllWindows()

def connect_to_db(path_to_database):
    conn = sqlite3.connect(path_to_database)
    return conn


def generate_password(length):
    sym = ":;/@#$%^&*(){}[]"
    all_char = ascii_uppercase + ascii_lowercase + digits + sym
    r = random.sample(all_char, length)
    password = "".join(r)
    return f"Your password is ready: [bold]{password}[/bold]"


def clear():
    os.system("clear")


def date():
    x = datetime.datetime.now().strftime("%H:%M:%S %b %d %Y")
    return x


def key(path_to_database):
    key_con = connect_to_db(path_to_database)
    cur = key_con.cursor()
    cur.execute("SELECT * FROM KEY")
    keys = cur.fetchall()
    for key in keys:
        key = "".join(key)
    return key


def cmd(command):
    os.system(command)


def play(path_to_music):
    playsound(path_to_music)


def play_using_sox(path_to_music):
    subprocess.call(["play", path_to_music])


def chdir(path_to_directory):
    os.chdir(path_to_directory)


def play_video(path_to_video):
    subprocess.call(["mplayer", path_to_video, "-fs"])


def insert(path_to_database, app, user, email, password):
    try:
        pass_con = connect_to_db(path_to_database)
        cur = pass_con.cursor()
        insertQuery = f"""INSERT INTO PASSWORDS VALUES (?, ?, ?, ?)"""
        cur.execute(insertQuery, (app.capitalize(), user, email, password))
        pass_con.commit()
        pass_con.close()
    except Exception as e:
        print("Oops Something Went Wrong")


def creds(path_to_database, app):
    apps = []
    usernames = []
    emails = []
    passwords = []
    try:
        pass_con = connect_to_db(path_to_database)
        cur = pass_con.cursor()
        cur.execute(f'SELECT * FROM PASSWORDS WHERE APPLICATION LIKE "%{app}%"')
        creds = cur.fetchall()
        for cred in creds:
            apps.append(cred[0])
            usernames.append(cred[1])
            emails.append(cred[2])
            passwords.append(cred[3])

        for (a, b, c, d) in zip(apps, usernames, emails, passwords):
            console.print(f'\nApplication     : [bold]{a}[/bold]')
            console.print(f'Username        : [bold]{b}[/bold]')
            console.print(f'Email/phone     : [bold]{c}[/bold]')
            console.print(f'Password        : [bold]{d}[/bold]')
    except sqlite3.Error as e:
        print(e)


def log_txt(path_to_log_dir, app, script, time):
    with open(f"{path_to_log_dir}/logs.log", "a") as f:
        # writing log
        f.write(
            f"\nTime: {time} Script: {script} Application: {app.capitalize()}")
        # closing file
        f.close()


def log(path_to_database, app, script, time):
    log_con = connect_to_db(path_to_database)
    cur = log_con.cursor()
    insertQuery = f"""INSERT INTO LOG VALUES (?, ?, ?)"""
    cur.execute(insertQuery, (app.capitalize(), time, __file__))
    log_con.commit()
    log_con.close()
