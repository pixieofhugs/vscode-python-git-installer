import subprocess
import shutil
import os

def is_git_installed():
    """Check if Git is installed and available in PATH."""
    return shutil.which("git") is not None
        

def install_git():
    """Download and install Git if not already installed."""
    if is_git_installed():
        print("Git is already installed. Skipping installation.")
        return
    print("Downloading Git...")
    git_url = "https://github.com/git-for-windows/git/releases/latest/download/Git-x86_64.exe"
    subprocess.run(["curl", "-L", git_url, "-o", "GitSetup.exe"])
    print("Installing Git...")
    subprocess.run(["GitSetup.exe", "/VERYSILENT", "/NORESTART"])
    os.remove("GitSetup.exe")

def is_git_configured():
    """Check if Git global username and email are configured."""
    try:
        username = subprocess.check_output(["git", "config", "--global", "user.name"], text=True).strip()
        email = subprocess.check_output(["git", "config", "--global", "user.email"], text=True).strip()
        return bool(username) and bool(email)
    except subprocess.CalledProcessError:
        return False

def configure_git_credentials():
    """Prompt user for Git credentials and configure them globally."""
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