#! /bin/bash

function tool() {
    if [ $(grep '^ID_LIKE' /etc/os-release) == "ID_LIKE=arch" ]; then
        if ! [ -x "$(`command -v figlet`)" ]; then
            echo "Error: figlet is not installed"
            echo "Installing figlet..."
            sudo pacman -Sy figlet
        else
            :
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
        else 
            :
        fi
        if ! [ -x "$(`command -v lolcat`)" ]; then
            echo "Error: lolcat is not installed"
            echo "Installing figlet..."
            sudo apt install lolcat
        else
            :
        fi
    fi
}

function install () {
    echo "Installing Script"
    sleep 1;
    echo "Moving Files"
    sudo cp manager.py /usr/local/bin/manager
    echo "To run the script type manager"
}

# sudo cp Bloody.flf /usr/share/figlet/fonts/

figlet -c -f Bloody "Munseer" | lolcat

FILE=/usr/local/bin/manager
if [[ -f $FILE ]]; then
    echo "Script Already Installed"
    exit
else
    FILE=~/.config/manager/
    if [ -d $FILE ];then
        echo "Directory $FILE Exists"
    else
        mkdir $FILE
    fi
    FILE1=~/.config/manager/log
    if [ -d $FILE1 ];then
        echo "Directory $FILE1 Exists"
    else
        mkdir $FILE1
    fi 
    FILE2=~/.config/manager/backup
    if [ -d $FILE2 ];then
        echo "Directory $FILE2 Exists"
    else
        mkdir $FILE2
    fi
    if [ -f ~/.config/manager/config.py ];then
        echo "Found Existing configuration"
    else
        cp config.py ~/.config/manager/
    fi
    if [ -f ~/.config/manager/db.sqlite3 ];then
        echo "Found Existing Database"
    else
        touch ~/.config/manager/db.sqlite3
    fi
    install
    # tool
fi

