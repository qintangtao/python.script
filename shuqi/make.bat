@echo off
set "bd=%cd%"
::echo %bd%
cd ..
set "bbd=%cd%"
::echo %bbd%
cd %bd%
::echo %cd%
if "%PYTHONPATH%" == "" ( 
	set PYTHONPATH=%bbd%;%PYTHONPATH%
)
::echo %PYTHONPATH%
pyrcc4 res.qrc -o res.py
call pyuic4 mainwindow.ui -o ui_mainwindow.py
pyinstaller -F -w -i bug.ico -n dump.exe --clean --key=shuqi123456 main.py
