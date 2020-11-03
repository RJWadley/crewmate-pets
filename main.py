import sys
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import QApplication
from colors import *
from crewmate import Crewmate

app = QApplication(sys.argv)

#get display size
display = app.primaryScreen()
screen = display.size()

crewmates = []
colors = ["Lime", "Red", "Cyan", "Orange", "Yellow"]

#ship keeps track of crewmates
def ship():

    # update display order if needed
    crewmatesort = crewmates[:]
    crewmatesort.sort(key=lambda x: x.y, reverse=False)
    if not (crewmatesort == crewmates):
        crewmates.sort(key=lambda x: x.y, reverse=False)
        for crewmate in crewmates:
            crewmate.raise_()

    #exit if no crewmates
    if len(crewmates) == 0:
        sys.exit()

    #remove crewmates that don't exist
    for i in range(len(crewmates)):
        if not crewmates[i].exists == True:
            crewmates.pop(i)
            break

    QTimer.singleShot(16, ship)

def init():
    for i in range(5):
        crewmate = Crewmate(colors[i], i, screen)
        crewmates.append(crewmate)
        crewmate.show()

    ship()

init()

sys.exit(app.exec_())
