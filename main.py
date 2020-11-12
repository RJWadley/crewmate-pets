import sys
import os
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import QApplication, QLabel, QMenu, QSystemTrayIcon
from ship import Ship

app = QApplication(sys.argv)

#get display size
display = app.primaryScreen()

label = QLabel("<font size=40>Loading Crewmates</font><br>This may take a while")
label.move(0,0)
label.setWindowTitle("Crewmates")
label.setWindowFlags(Qt.FramelessWindowHint)
#label.setAttribute(Qt.WA_TranslucentBackground)
label.show()

if getattr(sys, 'frozen', False):
    icon = QIcon(os.path.join(sys._MEIPASS, "icon/Crewmate.ico"))
else:
    icon = QIcon("Crewmate.ico")
menu = QMenu()
exitAction = menu.addAction("Exit")
exitAction.triggered.connect(sys.exit)

tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setContextMenu(menu)
tray.show()

if not os.path.exists(os.path.join("img", "default", "idle.png")):
    warning = QLabel("<font size=40>Could not find images</font><br>Exiting in 5 seconds")
    warning.setWindowTitle("Unable to Start")
    warning.setWindowFlags(Qt.FramelessWindowHint)
    warning.show()

    QTimer.singleShot(5000, sys.exit)

mothership = Ship(8, display)

QTimer.singleShot(5000, label.destroy)

sys.exit(app.exec_())
