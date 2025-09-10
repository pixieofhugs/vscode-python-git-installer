# PowerShell Dev Environment Bootstrapper for Windows
# Installs Python, Git, VS Code, configures Git, and updates PATH

function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal $currentUser
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-Admin)) {
    Write-Host "Script is not running as administrator. Relaunching with elevated privileges..."
    $scriptPath = $MyInvocation.MyCommand.Definition
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" -Verb RunAs
    exit
}

function Install-PackageIfMissing {
    param(
        [string]$ExeName,
        [string]$Url,
        [string]$InstallerArgs
    )
    if (-not (Get-Command $ExeName -ErrorAction SilentlyContinue)) {
        $file = "$env:TEMP\$ExeName-setup.exe"
        Write-Host "Downloading $ExeName..."
        Invoke-WebRequest -Uri $Url -OutFile $file
        Write-Host "Installing $ExeName..."
        Start-Process -FilePath $file -ArgumentList $InstallerArgs -Wait -Verb RunAs
        Remove-Item $file
    } else {
        Write-Host "$ExeName is already installed. Skipping."
    }
}

# Install Python
Install-PackageIfMissing -ExeName "python" -Url "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe" -InstallerArgs "/quiet InstallAllUsers=1 PrependPath=1"

# Install Git
Install-PackageIfMissing -ExeName "git" -Url "https://github.com/git-for-windows/git/releases/latest/download/Git-x86_64.exe" -InstallerArgs "/VERYSILENT /NORESTART"

# Install VS Code
Install-PackageIfMissing -ExeName "code" -Url "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64" -InstallerArgs "/silent /mergetasks=!runcode"

# Install GitHub Desktop
Install-PackageIfMissing -ExeName "github" -Url "https://central.github.com/deployments/desktop/desktop/latest/win32" -InstallerArgs "/silent"

# Add Git, Python, and Python Scripts to system PATH
function Add-ToSystemPath {
    param([string]$NewPath)
    $reg = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    $current = (Get-ItemProperty -Path $reg -Name Path).Path
    if ($current -notlike "*$NewPath*") {
        Set-ItemProperty -Path $reg -Name Path -Value ($current + ";" + $NewPath)
        Write-Host "Added $NewPath to system PATH. You may need to restart for changes to take effect."
    } else {
        Write-Host "$NewPath is already in system PATH."
    }
}

# Typical install paths
$gitPath = "C:\Program Files\Git\cmd"
$pythonPath = (Get-Command python).Source | Split-Path
$pythonScriptsPath = Join-Path $pythonPath 'Scripts'
Add-ToSystemPath -NewPath $gitPath
Add-ToSystemPath -NewPath $pythonPath
Add-ToSystemPath -NewPath $pythonScriptsPath

# Configure Git credentials
if (Get-Command git -ErrorAction SilentlyContinue) {
    $username = git config --global user.name
    $email = git config --global user.email
    if (-not $username) {
        $username = Read-Host "Enter your Git username"
        git config --global user.name "$username"
    } else {
        Write-Host "Git username already set: $username"
    }
    if (-not $email) {
        $email = Read-Host "Enter your Git email"
        git config --global user.email "$email"
    } else {
        Write-Host "Git email already set: $email"
    }
} else {
    Write-Host "Git is not installed. Skipping Git credential configuration."
}

# Prompt user to sign in to VS Code
if (Get-Command code -ErrorAction SilentlyContinue) {
    Write-Host "Launching VS Code. Please sign in (bottom left 'Accounts' icon)."
    Start-Process code
} else {
    Write-Host "VS Code is not installed. Skipping sign-in prompt."
}

# Install VS Code extensions from vscode-extensions.txt if VS Code is installed
$extensionsFile = Join-Path $PSScriptRoot 'vscode-extensions.txt'
if (Get-Command code -ErrorAction SilentlyContinue -OutVariable codeCmd) {
    if (Test-Path $extensionsFile) {
        $extensions = Get-Content $extensionsFile | Where-Object { $_ -and -not $_.StartsWith('#') }
        foreach ($ext in $extensions) {
            Write-Host "Installing VS Code extension: $ext"
            & $codeCmd.Source --install-extension $ext
        }
    } else {
        Write-Host "No vscode-extensions.txt file found. Skipping extension install."
    }
} else {
    Write-Host "VS Code is not installed. Skipping extension install."
}

Write-Host "All installations and configurations completed successfully."
