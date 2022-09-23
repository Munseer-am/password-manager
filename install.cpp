#include <iostream>
#include <filesystem>
#include <unistd.h>
#include <sys/types.h>
#include <bits/stdc++.h>
#include <pwd.h>
using namespace std;

int is_installed(string tool) {
    int result = system(("command -v " + tool + " >/dev/null").c_str());
    return result;
}

int install(string tool) {
    if (is_installed("apt") == 0) {
        system(("sudo apt install " + tool + " -y").c_str());
    }
    else if (is_installed("pacman") == 0) {
        system(("sudo pacman -Sy " + tool).c_str());
    }
    else if (is_installed("dnf") == 0) {
        system(("sudo dnf install " + tool).c_str());
    }
    else {
        cout << "No tool for installation found";
        return 1;
    }
    return 0;
}

int file_exists(string path) {
    return filesystem::is_regular_file(path);
}

int directory_exists(string path) {
    return filesystem::is_directory(path);
}

int tool() {
    if (is_installed("figlet") != 0) {
        cout << "Error: figlet is not installed\n";
        cout << "Installing figlet...\n";
        install("figlet");
        tool();
    }
    else if (is_installed("lolcat") != 0) {
        cout << "Error: lolcat is not installed\n";
        cout << "Installing lolcat...\n";
        install("lolcat");
    }
    return 0;
}

int main() {
    struct passwd *pw = getpwuid(getuid());
    const char *homedir = pw->pw_dir;
    string home = string(homedir);
    tool();
    system("clear");
    system("figlet -c -f Bloody 'Munseer' | lolcat");
    if (file_exists("/usr/local/bin/manager") != 1) {
        cout << "Installing Script\n";
        sleep(1);
        system("sudo cp manager.py /usr/local/bin/manager");
        cout << "Creating Required Directories\n";
        sleep(0.9);
        if (directory_exists("/usr/share/figlet/fonts/") != 0) {
            system("sudo cp Bloody.flf /usr/share/figlet/fonts");
        }
        else {
            system("sudo cp Bloody.flf /usr/share/figlet/");
        }
        if (directory_exists(home+"/.config/manager/") != 1) {
            filesystem::create_directory(home+"/.config/manager");
        }
        if (directory_exists(home+"/.config/manager/log/") != 1) {
            filesystem::create_directory(home+"/.config/manager/log/");
        }
        if (directory_exists(home+"/.config/manager/backup/") != 1) {
            filesystem::create_directory(home+"/.config/manager/backup/");
        }
        cout << "Moving Files\n";
        sleep(0.5);
        if (file_exists(home+"/.config/manager/config.py") != 1) {
            filesystem::copy("config.py", home+"/.config/manager/");
        }
        else {
            cout << "Found Existing Configuration\n";
        }
        if (file_exists(home+"/.config/manager/db.sqlite3") == 1) {
            cout << "Found Existing Database\n";
        }
        sleep(0.4);
        if (file_exists(home+"/.config/manager/menu.py") != 1) {
            filesystem::copy("menu.py", home+"/.config/manager/");
        }
        cout << "To run the script type 'manager'" << endl;
    }
    else {
        cout << "Script Already Installed" << endl;
        exit(0);
    }
}
