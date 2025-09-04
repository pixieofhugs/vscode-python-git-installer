"""
Main entry point for the VS Code, Python, and Git installer/configurator.
"""

from installers.vscode import install_vscode, prompt_vscode_sign_in
from installers.python_installer import install_python
from installers.git_installer import install_git, configure_git_credentials
from utils.env import ensure_paths

def main():
    """Run the installation and configuration steps."""
    install_vscode()
    install_python()
    install_git()
    ensure_paths()
    configure_git_credentials()
    prompt_vscode_sign_in()
    print("All installations and configurations completed successfully.")

if __name__ == "__main__":
    main()