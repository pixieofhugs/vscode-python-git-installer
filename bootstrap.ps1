# PowerShell bootstrap script for Windows
# Usage: .\bootstrap.ps1

# Function to check if running as administrator
function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal $currentUser
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Relaunch as admin if not already
if (-not (Test-Admin)) {
    Write-Host "Script is not running as administrator. Relaunching with elevated privileges..."
    $scriptPath = $MyInvocation.MyCommand.Definition
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" -Verb RunAs
    exit
}

# Check for Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $python) {
    Write-Host "Python not found. Downloading and installing Python..."
    $pythonUrl = "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe"
    $installerPath = "$env:TEMP\PythonSetup.exe"
    Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
    Write-Host "Running Python installer..."
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait -Verb RunAs
    Remove-Item $installerPath
    $env:Path += ";$env:LOCALAPPDATA\Microsoft\WindowsApps"
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        $python = Get-Command python3 -ErrorAction SilentlyContinue
    }
    if (-not $python) {
        Write-Error "Python installation failed. Please install Python manually."
        exit 1
    }
}

# Upgrade pip and install dependencies
Write-Host "Installing Python dependencies..."
& $python.Source -m pip install --upgrade pip
& $python.Source -m pip install -r requirements.txt

# Run main.py
Write-Host "Running main.py..."
& $python.Source src/main.py
