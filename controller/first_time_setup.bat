@ECHO OFF
ECHO Type "free" when prompted for password
if exist "%TEMP%\freeride_setup\" rmdir "%TEMP%\freeride_setup\" /s /q
mkdir %TEMP%\freeride_setup
for /f "usebackq tokens=3 delims=," %%a in (`getmac /fo csv /v ^| find "Bluetooth"`) do set MAC=%%~a
ECHO %MAC% > %TEMP%\freeride_setup\mymac.txt
powershell -Command "(gc %TEMP%\freeride_setup\mymac.txt) -replace '-', ':' | Out-File -encoding ASCII %TEMP%\freeride_setup\mymac.txt"
scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=NUL: %TEMP%\freeride_setup\mymac.txt pi@freeridecontroller.local: