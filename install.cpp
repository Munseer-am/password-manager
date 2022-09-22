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

int path_exists(string path) {
    if (filesystem::is_regular_file(path)) {
        bool result = filesystem::is_regular_file(path);
        return result;
    }
    else if (filesystem::is_regular_file(path) != 1) {
        bool result = filesystem::is_directory(path);
        return result;
    }
    else {
        return false;
    }
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
}
