import clipboard
import os
import sys
from cryptography.fernet import Fernet
from functools import cache
from hashlib import sha256
from random import sample
from rich.console import Console
from rich.prompt import Prompt
from shutil import copyfile
from string import ascii_lowercase, ascii_uppercase, digits

sys.path.insert(0, os.path.join(os.path.expanduser("~") + "/.config/manager/"))
from config import config
from menu import menu

console = Console()


@cache
def generate_password():
    sym = "!@#$%^&*()[]{}:;"
    all_chars = ascii_uppercase + ascii_lowercase + sym + digits
    r = sample(all_chars, 20)
    return "".join(r)


@cache
def sha256_encoder(word: str):
    enc = sha256(word.encode("utf-8")).hexdigest()
    return enc


@cache
def copy(word: str):
    clipboard.copy(word)
    clipboard.paste()


@cache
def is_configured():
    if config is not None:
        return False
    else:
        return True


@cache
def uninstall_script():
    pas = Prompt.ask("Enter password to delete", password=True)
    hashed = sha256_encoder(pas)
    if hashed != config["KEY"]:
        console.print("Invalid Password")
    else:
        os.system("sudo rm /usr/local/bin/manager")


@cache
def encrypt(key: bytes, password: str):
    enc = Fernet(key)
    return enc.encrypt(password.encode("utf-8"))


@cache
def decrypt(key: bytes, password: bytes):
    dec = Fernet(key)
    return dec.decrypt(password).decode("utf-8")


@cache
def backup(db: str, path: str, dst: str):
    copyfile(path, os.path.join(dst + "/" + db))
