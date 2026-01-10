# PowerShell script to create a desktop shortcut for PDF Editor
# Run this script to create a shortcut on your desktop

# Get the current directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Create shortcut on Desktop
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "PDF Editor.lnk"

# Create WScript Shell object
$WshShell = New-Object -ComObject WScript.Shell

# Create the shortcut
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Set target to the VBS launcher (no console window)
$Shortcut.TargetPath = Join-Path $ScriptDir "Launch_PDF_Editor.vbs"

# Set working directory
$Shortcut.WorkingDirectory = $ScriptDir

# Set description
$Shortcut.Description = "Launch PDF Editor Application"

# Optional: Set icon (Windows will use default VBS icon if not specified)
# You can download a PDF icon and uncomment this line:
# $Shortcut.IconLocation = Join-Path $ScriptDir "pdf_icon.ico"

# Save the shortcut
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully at: $ShortcutPath" -ForegroundColor Green
Write-Host ""
Write-Host "To pin to taskbar:" -ForegroundColor Yellow
Write-Host "1. Right-click the desktop shortcut" -ForegroundColor Cyan
Write-Host "2. Select 'Pin to taskbar'" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
