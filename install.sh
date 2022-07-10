#! /bin/bash
figlet -c -f Bloody "Munseer" | lolcat

echo "WARNING: First run python manager.py before running this script to set password"

if [[ $(whoami) != "root" ]]; then
    echo "Try running script as root"
    exit
else
    :
fi

FILE=/usr/local/bin/manager
if [[ -f $FILE ]]; then
    echo "Script Already Installed"
    exit
else
    :
fi

echo "Installing Script..."
sleep 2;

echo "Moving Files..."
cp manager.py /usr/local/bin/manager
cp menu.py config.py /usr/local/bin/
cp Bloody.flf /usr/share/figlet/fonts

sleep 1;

echo "Changing Permission"
chmod +x /usr/local/bin/manager

echo "To run script enter manager"
exit
