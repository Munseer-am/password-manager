import os
import re
import db
import random
import base64
import hashlib
import datetime
import clipboard
from string import *
from insults import insult
from shutil import copyfile
from typing import Callable
from rich.table import Table
from rich.prompt import Prompt
from rich.console import Console
from cryptography.fernet import Fernet

console: Console = Console()
salt: bytes = os.urandom(16)

def dateTime() -> None:
    x = str(datetime.datetime.now().strftime("%H:%M:%S %b %d %Y"))
    print(x)

def ask(*args, **kwargs):
    return Prompt.ask(*args, **kwargs)

def passGen(length=20) -> str:
    chars: str = ascii_lowercase + ascii_uppercase + digits + "!@#$%^&*()_+:|~"
    return "".join(random.sample(chars, length))

def encoder(word: str, hash: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(hash, word.encode("UTF-8"), salt, 1000)

def copy(word: str) -> None:
    clipboard.copy(word)
    clipboard.paste()

def encrypt(key: bytes, password: str) -> bytes:
    enc: Fernet = Fernet(key)
    return enc.encrypt(password.encode("utf=8"))

def decrypt(key: bytes, password: bytes) -> bytes:
    enc: Fernet = Fernet(key)
    return enc.decrypt(password)

def b64_encode(token: bytes) -> bytes:
    return base64.b64encode(token)

def b64_decode(token: bytes) -> str:
    return base64.b64decode(token).decode()

def isValidEmail(email: str) -> bool:
    regex: str = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(regex, email):
        return True
    return False

def security(key: bytes, func: Callable, *args, **kwargs) -> None:
    i: int = 0
    inp: str = ask("Enter password", password=True)
    enc: bytes = encoder(inp, "sha256", salt)
    while enc != key:
        i += 1
        if i >= 3:
            console.print("Access Denied!")
            break
        else:
            console.print(insult())
            inp: str = ask("\nTry again", password=True)
            enc: bytes = encoder(inp, "sha256", salt)
    else:
        console.print("Access Granted!")
        func(*args, **kwargs)

def backup(src_path: str, dst_path: str) -> None:
    copyfile(src_path, dst_path)

def printTable(title: str, columns: list, data: list) -> Table:
    table: Table = Table(title=title)
    for column in columns:
        table.add_column(column, style="cyan", no_wrap=True)
    for d in data:
        d: list = [str(t) for t in d]
        table.add_row(*d)
    return table

def sub_print(text, leading_spaces=0):
    text_chars: list = list(text)
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
