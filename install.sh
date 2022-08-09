#! /bin/bash

function tool() {
    if [ $(grep '^ID_LIKE' /etc/os-release) == "ID_LIKE=arch" ]; then
        if ! [ -x "$(`command -v figlet`)" ]; then
            echo "Error: figlet is not installed"
            echo "Installing figlet..."
            sudo pacman -Sy figlet
        else
        echo "Figlet is installed"
        fi
        if ! [ -x "$(`command -v lolcat`)" ]; then
            echo "Error: lolcat is not installed"
            echo "Installing lolcat..."
            sudo pacman -Sy lolcat
        else
            :
        fi
    else
        if ! [ -x "$(`command -v figlet`)" ]; then
            echo "Error: figlet is not installed"
            echo "Installing figlet..."
            sudo apt install figlet
        fi
        if ! [ -x "$(`command -v lolcat`)" ]; then
            echo "Error: lolcat is not installed"
            echo "Installing figlet..."
            sudo apt install lolcat
        fi
    fi
}

function install () {
    echo "Installing Script"
    sleep 1;
    echo "Moving Files"
    sudo cp manager.py /usr/local/bin/manager
    cp config.py menu.py /home/munseer/.config/manager
    touch ~/.config/manager/db.sqlite3
    echo "Changing Permission"
    sudo chmod +x /usr/local/bin/manager
    echo "To run the script type manager"
}

sudo cp Bloody.flf /usr/share/figlet/fonts/

figlet -c -f Bloody "Munseer" | lolcat

FILE=/usr/local/bin/manager
if [[ -f $FILE ]]; then
    echo "Script Already Installed"
    exit
else
    mkdir ~/.config/manager/
    mkdir ~/.config/manager/log
    mkdir ~/.config/manager/backup/
    install
    tool
fi

