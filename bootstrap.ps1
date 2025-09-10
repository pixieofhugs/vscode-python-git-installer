# PowerShell bootstrap script for Windows
# Usage: .\bootstrap.ps1

# Check for Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $python) {
    Write-Host "Python not found. Installing Python via winget..."
    winget install -e --id Python.Python.3
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
