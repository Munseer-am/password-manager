#include <iostream>
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

int main() {
    string tool;
    cout << "Enter a command: ";
    getline(cin, tool);
    is_installed(tool);
    return 0;
}
