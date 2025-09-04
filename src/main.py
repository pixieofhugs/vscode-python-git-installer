import os
import subprocess
import sys
import shutil

def is_vscode_installed():
    return shutil.which("code") is not None

def is_python_installed():
    return shutil.which("python") is not None or shutil.which("python3") is not None

def is_git_installed():
    return shutil.which("git") is not None

def is_git_configured():
    try:
        username = subprocess.check_output(["git", "config", "--global", "user.name"], text=True).strip()
        email = subprocess.check_output(["git", "config", "--global", "user.email"], text=True).strip()
        return bool(username) and bool(email)
    except subprocess.CalledProcessError:
        return False

def download_and_install_vscode():
    if is_vscode_installed():
        print("Visual Studio Code is already installed. Skipping installation.")
        return
    print("Downloading Visual Studio Code...")
    vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64"
    subprocess.run(["curl", "-L", vscode_url, "-o", "VSCodeSetup.exe"])
    print("Installing Visual Studio Code...")
    subprocess.run(["VSCodeSetup.exe", "/silent", "/mergetasks=!runcode"])
    os.remove("VSCodeSetup.exe")

def download_and_install_python():
    if is_python_installed():
        print("Python is already installed. Skipping installation.")
        return
    print("Downloading Python...")
    python_url = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
    subprocess.run(["curl", "-L", python_url, "-o", "PythonSetup.exe"])
    print("Installing Python...")
    subprocess.run(["PythonSetup.exe", "/quiet", "InstallAllUsers=1", "PrependPath=1"])
    os.remove("PythonSetup.exe")

def download_and_install_git():
    if is_git_installed():
        print("Git is already installed. Skipping installation.")
        return
    print("Downloading Git...")
    git_url = "https://github.com/git-for-windows/git/releases/latest/download/Git-x86_64.exe"
    subprocess.run(["curl", "-L", git_url, "-o", "GitSetup.exe"])
    print("Installing Git...")
    subprocess.run(["GitSetup.exe", "/VERYSILENT", "/NORESTART"])
    os.remove("GitSetup.exe")

def configure_git_credentials():
    if not is_git_installed():
        print("Git is not installed. Skipping Git credential configuration.")
        return
    if is_git_configured():
        print("Git credentials are already configured. Skipping configuration.")
        return
    print("\nConfiguring Git credentials...")
    username = input("Enter your Git username: ")
    email = input("Enter your Git email: ")
    subprocess.run(["git", "config", "--global", "user.name", username])
    subprocess.run(["git", "config", "--global", "user.email", email])
    print("Git credentials configured.")

def prompt_vscode_sign_in():
    if not is_vscode_installed():
        print("VS Code is not installed. Skipping sign-in prompt.")
        return
    print("\nLaunching VS Code for sign-in...")
    subprocess.Popen(["code"])
    print("Please sign in to your account in VS Code (bottom left 'Accounts' icon).")

def main():
    download_and_install_vscode()
    download_and_install_python()
    download_and_install_git()
    configure_git_credentials()
    prompt_vscode_sign_in()
    print("All installations and configurations completed successfully.")

if __name__ == "__main__":
    main()