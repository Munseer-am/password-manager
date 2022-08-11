# _Password Manager Using Python And Sqlite3_

## _**Installation**_

#### _1. First git clone this repository_
#### _2. Run install.sh script as root_
#### _3. Type `manager` to run the script_
#### _4. Enter the details_

## _**How to reset password**_
#### _If you lost or forgot your password you can reset password using command line arguments_

#### _Just type `manager --reset` or `manager -r` and enter the email address that you gave during the first setup_
>_**Warning:** This will not work correctly everytime. Do backup your password_ 

## _**How to uninstall the script**_
#### _To delete the script from bin folder use `manager -U` or `manager --uninstall` to remove the script_
>_**Note:** It will not remove the config files that was created during the installation_

## _**Warnings**_
#### _**1. If you changed or removed the `ENCRYPTION_KEY` your passwords cannot be encrypted or decrypted and password manager will give you a lot of errors.**_
#### _**2. For the first you run the script it will create required directory and files. If you delete the manager script from the location `/usr/local/bin/` the config files will remain.**_
#### _**3. ~~Due to the remaining of the config files and directories. When you try to install the script second time the `install.sh` script will give error that the directories already exists. But it will not affect the installation~~**_

#### _**4. Sometimes when running `install.sh` the script will stuck in some process. If it is stuck for more than 1 to 2 min force quit the script by pressing `ctrl+c`. There will be no problem with the installation. This happens while the script checks if the necessary tools are installed.**_
>_**Notes:** If the script fails install the following tools `figlet` and `lolcat` using `apt install figlet lolcat` or `pacman -Sy figlet lolcat`_

#### _**5. If you installed it and deleted the manager. When you run the `install.sh` script it will override the existing database and config file. So backup your config.py file somewhere in your system. Copy it to the location `~/.config/manager/`.**_
