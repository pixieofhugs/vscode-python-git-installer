import os
import subprocess
import sys

def download_and_install_vscode():
    print("Downloading Visual Studio Code...")
    vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64"
    subprocess.run(["curl", "-L", vscode_url, "-o", "VSCodeSetup.exe"])
    print("Installing Visual Studio Code...")
    subprocess.run(["VSCodeSetup.exe", "/silent", "/mergetasks=!runcode"])
    os.remove("VSCodeSetup.exe")

def download_and_install_python():
    print("Downloading Python...")
    python_url = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
    subprocess.run(["curl", "-L", python_url, "-o", "PythonSetup.exe"])
    print("Installing Python...")
    subprocess.run(["PythonSetup.exe", "/quiet", "InstallAllUsers=1", "PrependPath=1"])
    os.remove("PythonSetup.exe")

def download_and_install_git():
    print("Downloading Git...")
    git_url = "https://github.com/git-for-windows/git/releases/latest/download/Git-x86_64.exe"
    subprocess.run(["curl", "-L", git_url, "-o", "GitSetup.exe"])
    print("Installing Git...")
    subprocess.run(["GitSetup.exe", "/VERYSILENT", "/NORESTART"])
    os.remove("GitSetup.exe")

def prompt_vscode_sign_in():
    print("\nLaunching VS Code for sign-in...")
    subprocess.Popen(["code"])
    print("Please sign in to your account in VS Code (bottom left 'Accounts' icon).")

def main():
    download_and_install_vscode()
    download_and_install_python()
    download_and_install_git()
    prompt_vscode_sign_in()
    print("All installations completed successfully.")

if __name__ == "__main__":
    main()