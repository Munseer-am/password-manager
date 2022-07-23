# _Password Manager Using Python And Sqlite3_

## _**Installation**_

#### _1. First git clone this repository_
#### _2. Run install.sh script as root_
#### _3. Type `manager` to run the script_
#### _4. Enter the details_

## _**How to reset password**_
#### _If you lost or forgot your password you can reset password using command line arguments_
#### _Just type `manager reset` and enter the email address that you gave during the first setup_
>_**Warning:** This will not work correctly everytime. Do backup your password_ 

## _**Warnings**_
#### _**1. If you changed or removed the `ENCRYPTION_KEY` your passwords cannot be encrypted or decrypted and password manager will give you a lot of errors.**_
#### _**2. For the first you run the script it will create required directory and files. If you delete the manager script from the location `/usr/local/bin/` the config files will remain.**_
#### _**3. Due to the remaining of the config files and directories. When you try to install the script second time the `install.sh` script will give error that the directories already exists. But it will not affect the installation**_

