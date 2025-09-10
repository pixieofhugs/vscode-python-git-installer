"""
Main entry point for the VS Code, Python, and Git installer/configurator.
"""

import sys
import os
import ctypes
import subprocess

def ensure_admin():
    """
    Relaunch the script with administrator privileges if not already running as admin.
    """
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False
        python_exe = sys.executable
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
        command = f'Start-Process "{python_exe}" -ArgumentList \'"{script}" {params}\' -Verb RunAs'
        subprocess.run(['powershell', '-Command', command])
        sys.exit()

ensure_admin()

from installers.vscode import install_vscode, prompt_vscode_sign_in
from installers.git_installer import install_git, configure_git_credentials
from utils.env import ensure_paths

def main():
    """Run the installation and configuration steps."""
    install_vscode()
    install_git()
    ensure_paths()
    configure_git_credentials()
    prompt_vscode_sign_in()
    print("All installations and configurations completed successfully.")

if __name__ == "__main__":
    main()