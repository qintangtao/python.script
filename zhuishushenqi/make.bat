
pyrcc4 res.qrc -o res.py
call pyuic4 mainwindow.ui -o ui_mainwindow.py
pyinstaller -F -w -i bug.ico -n dump.exe --clean --key=zhuishushengqi123456 main.py