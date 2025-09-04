import subprocess
import shutil
import os

def is_python_installed():
    """Check if Python is installed and available in PATH."""
    return shutil.which("python") is not None or shutil.which("python3") is not None

def install_python():
    """Download and install Python if not already installed."""
    if is_python_installed():
        print("Python is already installed. Skipping installation.")
        return
    print("Downloading Python...")
    python_url = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
    subprocess.run(["curl", "-L", python_url, "-o", "PythonSetup.exe"])
    print("Installing Python...")
    subprocess.run(["PythonSetup.exe", "/quiet", "InstallAllUsers=1", "PrependPath=1"])
    os.remove("PythonSetup.exe")