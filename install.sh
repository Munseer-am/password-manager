#! /bin/bash

if [[ $(whoami) != root ]]; then
	echo "Try running script as root"
	exit
else
	:
fi

function install () {
    echo "Installing Script"
    sleep 1;
    echo "Moving Files"
    cp manager.py /usr/local/bin/manager
    # cp config.py menu.py ~/.config/manager
    echo "Changing Permission"
    chmod +x /usr/local/bin/manager
    echo "To run the script type manager"
}

if [ $(grep '^ID_LIKE' /etc/os-release) == "ID_LIKE=arch" ]; then
	if ! [ -x "$(command -v figlet)" ]; then
		echo "Error: figlet is not installed." >&2
		echo "Install figlet"
		sudo pacman -S figlet
	elif ! [ -x "$(command -v lolcat)" ]; then
		echo "Error: lolcat is not installed." >&2
		echo "Installing lolcat"
		sudo pacman -S lolcat
	else
		:
	fi
else
	if ! [ -x "$(command -v figlet)" ]; then
		echo "Error: figlet is not installed." >&2
		echo "Installing figlet"
		sudo apt-get install figlet
	elif ! [ -x "$(command -v lolcat)" ]; then
		echo "Error: lolcat is not installed." >&2
		echo "Installing lolcat"
		sudo apt-get install lolcat
	else
		:
	fi
fi

clear
cp Bloody.flf /usr/share/figlet/fonts/

figlet -c -f Bloody "Munseer" | lolcat

FILE=/usr/local/bin/manager
if [[ -f $FILE ]]; then
	echo "Script Already Installed"
	exit
else
  if [ -d ~/.config/manager/ ]; then
    if [ -d ~/.config/manager/log/ ]; then
      :
    else
      mkdir ~/.config/manager/log/
    fi
    if [ -d ~/.config/manager/backup/ ]; then
      :
    else
      mkdir ~/.config/manager/backup/
    fi
    install
  else
    mkdir ~/.config/manager/
    mkdir ~/.config/manager/log
    mkdir ~/.config/manager/backup/
    install
  fi
fi	
