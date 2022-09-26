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
        cout << "No Installation Tools Found";
        return 1;
    }
    return 0;
}

int file_exists(string file) {
    return filesystem::is_regular_file(file);
}

int directory_exists(string dir) {
    return filesystem::is_directory(dir);
}

int tool() {
    if (is_installed("figlet") != 0) {
        cout << "Error: figlet is not installed\n";
        cout << "Installing figlet...\n";
        install("figlet");
    }
    if (is_installed("lolcat") != 0) {
        cout << "Error: lolcat is not installed\n";
        cout << "Installing lolcat...\n";
    }
    return 0;
}

int install_font() {
    if (directory_exists("/usr/share/figlet/fonts/") != 0) {
        system("sudo cp Bloody.flf /usr/share/figlet/fonts");
    }
    else {
        system("sudo cp Bloody.flf /usr/share/figlet/");
    }
    return 0;
}

int main() {
    struct passwd *pw = getpwuid(getuid());
    const char *homedir = pw->pw_dir;
    string home = string(homedir);
    tool();
    install_font();
    system("clear");
    system("figlet -c -f Bloody 'Munseer' | lolcat");
    if (file_exists(home+"/.local/bin/manager") != 1) {
        cout << "Installing Script\n";
        system("cp manager.py ~/.local/bin/manager");
        system("chmod +x ~/.local/bin/manager");
        cout << "Creating Required Directories\n";
        if (directory_exists(home+"/.config/manager/") != 1) {
            filesystem::create_directory(home+"/.config/manager/");
        }
        if (directory_exists(home+"/.config/manager/log/") != 1) {
            filesystem::create_directory(home+"/.config/manager/log/");
        }
        if (directory_exists(home+"/.config/manager/backup/") != 1) {
            filesystem::create_directory(home+"/.config/manager/backup/");
        }
        cout << "Moving Files\n";
        if (file_exists(home+"/.config/manager/config.py") != 1) {
            filesystem::copy("lib/config.py", home+"/.config/manager/");
        }
        else {
            cout << "Found Existing Configuration\n";
        }
        if (file_exists(home+"/.config/manager/db.sqlite3") == 1) {
            cout << "Found Existing Database\n";
        }
        if (file_exists(home+"/.config/manager/menu.py") != 1) {
            filesystem::copy("lib/menu.py", home+"/.config/manager/");
        }
        system("cp install ~/.local/bin/manager_create");
        cout << "TO RUN THE SCRIPT TYPE `manager`" << endl;
    }
    else {
        if (directory_exists(home+"/.local/lib/python3.10/site-packages") == 1) {
            if (file_exists(home+"/.local/lib/python3.10/site-packages/config.py") != 1) {
                if (file_exists(home+"/.local/lib/python3.10/site-packages/config.py") != 1 && file_exists(home+"/.config/manager/config.py") == 1) {
                    filesystem::copy(home+"/.config/manager/config.py", home+"/.local/lib/python3.10/site-packages/");
                }
                else {
                    filesystem::copy("lib/config.py", home+"/.local/lib/python3.10/site-packages/");
                }
            }
            if (file_exists(home+"/.local/lib/python3.10/site-packages/menu.py") != 1) {
                if (file_exists(home+"/.local/lib/python3.10/site-packages/menu.py") != 1 && file_exists(home+"/.config/manager/menu.py") == 1) {
                    filesystem::copy(home+"/.config/manager/menu.py", home+"/.local/lib/python3.10/site-packages/");
                }
                else {
                    filesystem::copy("lib/menu.py", home+"/.local/lib/python3.10/site-packages/");
                }
            }
            if (file_exists(home+"/.config/manager/config.py") != 1) {
                if (file_exists(home+"/.config/manager/config.py") != 1 && file_exists(home+"/.local/lib/python3.10/site-packages/") == 1) {
                    filesystem::copy(home+"/.config/manager/config.py", home+"/.config/manager/");
                }
                else {
                    filesystem::copy("lib/config.py", home+"/.config/manager/");
                }
            }
        }
        cout << "Script Already Installed" << endl;
    }
}
