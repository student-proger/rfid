pyinstaller --icon=mainicon.ico --noconsole main.py
md dist\main\images
copy images\*.* dist\main\images\
copy license.txt dist\main\
rename dist\main\main.exe rfid.exe
rename dist\main\main.exe.manifest rfid.exe.manifest
