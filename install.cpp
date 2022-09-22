#include <iostream>
#include <filesystem>
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
    tool();
    if (directory_exists("/usr/share/figlet/fonts") == 10) {
        system("sudo cp Bloody.flf /usr/share/figlet/fonts");
    }
    else {
        system("sudo cp Bloody.flf /usr/share/figlet/");
    }
    system("clear");
    system("figlet -c -f Bloody 'Munseer' | lolcat");
    if (file_exists("/usr/local/bin/manager") == 1) {
        cout << "Script Already Installed" << endl;
        exit(0);
        // cout << "if executed\n";
        // cout << file_exists("/usr/local/bin/manager");
    }
    else {
        // cout << "Installing Script" << endl;
        cout << file_exists("/usr/local/bin/manager");
    }
}
