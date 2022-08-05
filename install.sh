#! /bin/bash

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

#if [ $(grep '^ID_LIKE' /etc/os-release) == "ID_LIKE=arch" ]; then
#	if ! [ -x "$(`command -v figlet`)" ]; then
#		echo "Error: figlet is not installed." >&2
#		echo "Installing figlet"
#		sudo pacman -Sy figlet
#	else
#		:
#
#	fi
#	if ! [ -x "$(`command -v lolcat`)" ]; then
#	  echo "Error: lolcat is not installed." >&2
#	  echo "Installing lolcat"
#	  sudo pacman -Sy lolcat
#	else
#	  :
#	fi
#else
#	if ! [ -x "$(`command -v figlet`)" ]; then
#		echo "Error: figlet is not installed." >&2
#		echo "Installing figlet"
#		sudo apt-get install figlet
#	else
#		:
#	fi
#	if ! [ -x "$(`command -v lolcat`)" ];then
#	  echo "Error: lolcat is not installed." >&2
#	  echo "Installing lolcat"
#	  sudo apt-get install lolcat
#	else
#	  :
#	fi
#fi
#
## clear
#cp Bloody.flf /usr/share/figlet/fonts/

#figlet -c -f Bloody "Munseer" | lolcat

FILE=/usr/local/bin/manager
if [[ -f $FILE ]]; then
	echo "Script Already Installed"
	exit
else
    mkdir ~/.config/manager/
    mkdir ~/.config/manager/log
    mkdir ~/.config/manager/backup/
    install
fi
