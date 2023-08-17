@echo off

REM Check if the destination directory exists
if not exist "c:\chromedriver\" (
    mkdir "c:\chromedriver\"
)

REM Copy the file, overwriting if it exists
copy /Y "h:\chromedriver\chromedriver.exe" "c:\chromedriver\chromedriver.exe"

REM Run the python script
H:\infoscreen\venv\Scripts\python.exe H:\infoscreen\src\main.py