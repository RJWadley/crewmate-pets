import sys
from PySide2.QtGui import *
from PySide2.QtCore import *
from colors import *
from crewmate import Crewmate
from imposter import Imposter

class Ship():

    def __init__(self, numCrewmates, display):
        self.crewmates = []
        colors = ["Lime", "Red", "Cyan", "Orange", "Yellow"]
        self.crewmates = []
        self.display = display
        self.screen = display.size()

        for i in range(numCrewmates - 1):
            crewmate = Crewmate(colors[i], i, self.screen)
            self.crewmates.append(crewmate)
            crewmate.show()

        self.imposter = Imposter(self.crewmates, colors[i + 1], i + 1, self.screen)
        self.crewmates.append(self.imposter)
        self.imposter.show()

        self.shipCycle()

    def shipCycle(self):
        # update display order if needed
        crewmatesort = self.crewmates[:]
        crewmatesort.sort(key=lambda x: x.y, reverse=False)
        if not (crewmatesort == self.crewmates):
            self.crewmates.sort(key=lambda x: x.y, reverse=False)
            for crewmate in self.crewmates:
                crewmate.raise_()

        #exit if no crewmates
        if len(self.crewmates) == 0:
            sys.exit()

        #remove crewmates that don't exist
        for i in range(len(self.crewmates)):
            if not self.crewmates[i].exists == True:
                self.crewmates.pop(i)
                break

        QTimer.singleShot(100, self.shipCycle)
