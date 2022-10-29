#! /bin/bash

function is_installed() {
    if ! command -v $1 &> /dev/null;then
        return 1
    else
        return 0
    fi
}

function install() {
    if is_installed apt; then
        sudo apt install $1 -y
    elif is_installed pacman; then
        sudo pacman -S $1
    elif is_installed dnf; then
        sudo dnf install $1
    else
        echo "No installation tools found"
    fi
}

function tool() {
    if ! is_installed figlet; then
        echo "Error: figlet is not installed"
        echo "Installing figlet..."
        install figlet
    elif ! is_installed lolcat; then
        echo "Error: lolcat is not installed"
        echo "Installing lolcat..."
        install lolcat
    fi
}

function move() {
    if [[ -f /usr/local/bin/manager ]]; then
        echo "Script Is Already installed"
        exit
    else
        echo "Installing Script"
        if ! [ -d ~/.config/manager ]; then
            mkdir ~/.config/manager/
        fi
        if ! [ -d ~/.config/manager/log/ ]; then
            mkdir ~/.config/manager/log/
        fi
        if ! [ -d ~/.config/manager/backup/ ]; then
            mkdir ~/.config/manager/backup/
        fi
        if [ -f ~/.config/manager/config.py ]; then
            echo "Found Existing Configuration"
        else
            cp config.py ~/.config/manager/
        fi
        if [ -f ~/.config/manager/db.sqlite3 ];then
            echo "Found Existing Database"
        else
            # touch ~/.config/manager/db.sqlite3
            :
        fi
        sleep 0.5;
        echo "Moving Files"
        sudo cp manager.py /usr/local/bin/manager
        cp menu.py ~/.config/manager/
        echo "To run the script type manager"
    fi
}

tool
clear
figlet -c -f Bloody "Munseer" | lolcat
echo "This Script Is Depricated"
