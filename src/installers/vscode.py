import subprocess
import shutil

def is_vscode_installed():
    """Check if VS Code is installed and available in PATH."""
    return shutil.which("code") is not None

def install_vscode():
    """Download and install VS Code if not already installed."""
    if is_vscode_installed():
        print("Visual Studio Code is already installed. Skipping installation.")
        return
    print("Downloading Visual Studio Code...")
    vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64"
    subprocess.run(["curl", "-L", vscode_url, "-o", "VSCodeSetup.exe"])
    print("Installing Visual Studio Code...")
    subprocess.run(["VSCodeSetup.exe", "/silent", "/mergetasks=!runcode"])
    os.remove("VSCodeSetup.exe")

def prompt_vscode_sign_in():
    """Launch VS Code and prompt user to sign in interactively."""
    if not is_vscode_installed():
        print("VS Code is not installed. Skipping sign-in prompt.")
        return
    print("\nLaunching VS Code for sign-in...")
    subprocess.Popen(["code"])
    print("Please sign in to your account in VS Code (bottom left 'Accounts' icon).")