import sys
from PySide2.QtCore import Qt, QTimer
from PySide2.QtWidgets import QApplication, QLabel
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


mothership = Ship(8, display)

QTimer.singleShot(5000, label.destroy)

sys.exit(app.exec_())
