import os
import sys

if len(sys.argv) < 2:
    print("Usage: python runas_admin.py <script_to_run.py> [args...]")
    sys.exit(1)

script = os.path.abspath(sys.argv[1])
args = ' '.join([f'"{arg}"' for arg in sys.argv[2:]])

# Use runas to launch the script as Administrator
# Note: This will prompt for the Administrator password if not already elevated
command = f'runas /user:Administrator "python \"{script}\" {args}"'
print(f"Running: {command}")
os.system(command)
