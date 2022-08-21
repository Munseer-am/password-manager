#! /bin/bash

function is_installed() {
    if ! command -v $1 &> /dev/null;then
        return 1
    else
        return 0
    fi
}

function tool() {
    if is_installed apt; then
        if is_installed figlet; then
            :
        else
            echo "Error: figlet is not installed"
            echo "Installing figlet..."
            sudo apt install figlet
        fi
        if is_installed lolcat; then
            :
        else
            echo "Error: lolcat is not installed"
            echo "Installing lolcat..."
            sudo apt install lolcat
        fi
    elif is_installed pacman; then
        if is_installed figlet; then
            :
        else
            echo "Error: figlet is not installed"
            echo "Installing figlet..."
            sudo pacman -Sy figlet
        fi
        if is_installed lolcat; then
            :
        else
            echo "Error: lolcat is not installed"
            echo "Installing lolcat..."
            sudo pacman -Sy lolcat
        fi
    elif is_installed dnf; then
        if is_installed figlet; then
            :
        else
            echo "Error: figlet is not installed"
            echo "Installing figlet..."
            sudo dnf install figlet
        fi
        if is_installed lolcat; then
            :
        else
            echo "Error: lolcat is not installed"
            echo "Installing lolcat..."
            sudo dnf install lolcat
        fi
    else
        :
    fi
}

tool
clear
figlet -c -f Bloody "Munseer" | lolcat

function install () {
    echo "Installing Script"
    sleep 1;
    echo "Moving Files"
    if [ -d /usr/share/figlet/fonts ];then
        sudo cp Bloody.flf /usr/share/figlet/fonts
    else
        sudo cp Bloody.flf /usr/share/figlet/
    fi
    sudo cp manager.py /usr/local/bin/manager
    cp menu.py ~/.config/manager/

    echo "To run the script type manager"
}

# figlet -c -f Bloody "Munseer" | lolcat

FILE=/usr/local/bin/manager
if [[ -f $FILE ]]; then
    echo "Script Already Installed"
    exit
else
    FILE=~/.config/manager/
    if [ -d $FILE ];then
        # echo "Directory $FILE Exists"
        :
    else
        mkdir $FILE
    fi
    FILE1=~/.config/manager/log
    if [ -d $FILE1 ];then
        # echo "Directory $FILE1 Exists"
        :
    else
        mkdir $FILE1
    fi 
    FILE2=~/.config/manager/backup
    if [ -d $FILE2 ];then
        # echo "Directory $FILE2 Exists"
        :
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

