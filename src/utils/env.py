import os
import sys
import winreg
import ctypes
import subprocess

def is_admin():
    """
    Check if the script is running with administrator privileges.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    """
    Relaunch the current script with administrator privileges.
    """
    print("Restarting script as administrator...")
    python_exe = sys.executable
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
    command = f'Start-Process "{python_exe}" -ArgumentList \'"{script}" {params}\' -Verb RunAs'
    subprocess.run(['powershell', '-Command', command])
    sys.exit()

def add_to_system_path(new_path):
    """
    Add a directory to the Windows system PATH if not already present.
    Assumes script is running as administrator.
    """
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                        0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
        value, _ = winreg.QueryValueEx(key, "Path")
        paths = value.split(";")
        if new_path not in paths:
            paths.append(new_path)
            new_value = ";".join(paths)
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_value)
            print(f"Added {new_path} to system PATH. You may need to restart for changes to take effect.")
        else:
            print(f"{new_path} is already in system PATH.")

def get_git_install_path():
    """Return the typical install path for Git on Windows, if it exists."""
    possible_paths = [
        r"C:\Program Files\Git\cmd",
        r"C:\Program Files (x86)\Git\cmd"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def get_python_install_path():
    """Return the directory containing python.exe, if found."""
    import shutil
    python_path = shutil.which("python")
    if python_path:
        return os.path.dirname(python_path)
    return None

def ensure_paths():
    """Ensure Git and Python install directories are in the system PATH."""
    git_path = get_git_install_path()
    if git_path:
        add_to_system_path(git_path)
    else:
        print("Could not find Git install path.")

    python_path = get_python_install_path()
    if python_path:
        add_to_system_path(python_path)
    else:
        print("Could not find Python install path.")