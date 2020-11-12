import sys
from PySide2.QtWidgets import QApplication
from ship import Ship

app = QApplication(sys.argv)

#get display size
display = app.primaryScreen()

mothership = Ship(5, display)

sys.exit(app.exec_())
