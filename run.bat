@echo off
setlocal

:: Set the Python script filename
set PYTHON_SCRIPT=baud_rate_brute.py

:: Check if the script is running with administrative privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrative privileges...
) else (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%0' -Verb RunAs"
    exit /b
)

:: Set the working directory to the location of the batch file
cd /d "%~dp0"

:: Check for required Python packages and install them if necessary
echo Checking for required Python packages...
pip list | findstr "pyserial colorama" >nul 2>&1
if %errorLevel% neq 0 (
    echo Installing required Python packages...
    pip install pyserial colorama
)

:: Display message and clear the screen
echo Running Python script...
cls

:: Run the Python script
python %PYTHON_SCRIPT%

:: Keep the command window open
echo.
echo Press any key to exit...
pause >nul

endlocal
