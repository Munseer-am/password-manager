#! /bin/bash

if [[ $(whoami) != "root" ]];then
	echo "Try running script as root"
	exit
else
	:
fi

FILE=/usr/local/bin/manager
if [[ -f "$FILE" ]];then
	echo "Script Already Installed"
	exit
else
	:
fi

echo "Installiing Script..."
sleep 2;

echo "Edit Config File"
sleep 1;

nano config.py
echo "Closing nano"
sleep 2;
echo "Moving Files"
cp myModule.py config.py /usr/local/bin/
cp manager.py /usr/local/bin/manager

sleep 1;
echo "Changing Permission"
chmod +x /usr/local/bin/manager

echo "TO run script enter manager"
