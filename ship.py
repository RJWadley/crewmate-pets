import sys
import math
import random
from PySide2.QtGui import *
from PySide2.QtCore import *
from colors import *
from crewmate import Crewmate
from imposter import Imposter

class Ship():

    def __init__(self, numCrewmates, display):
        self.numCrewmates = numCrewmates
        self.crewmates = []
        self.crewmates = []
        self.display = display
        self.screen = display.size()
        self.meeting = False
        self.sus = None
        self.crewmatesAlive = False

        QTimer.singleShot(10, self.populateShip)

    def populateShip(self):
        colors = ["Lime", "Red", "Cyan", "Orange", "Yellow", "Purple", "Pink", "Blue"]
        random.shuffle(colors)
        #fixme print(colors[numCrewmates - 1])
        for i in range(self.numCrewmates - 1):
            crewmate = Crewmate(colors[i], i, self.screen)
            self.crewmates.append(crewmate)
            crewmate.show()

        self.imposter = Imposter(self, colors[i + 1], i + 1, self.screen)
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
        #restart if needed
        if (len(self.crewmates) <= 2 or self.imposter.dead == True or self.imposter.exists == False) and self.meeting == False:
            for crewmate in self.crewmates:
                crewmate.speed = 1
                crewmate.progress = -999
                crewmate.destination = [-200, random.randrange(0,self.screen.height())]
            QTimer.singleShot(3000, self.restart)
            return
        #restart if all crewmates dead
        self.crewmatesAlive = False
        for crewmate in self.crewmates:
            if crewmate.dead == False and not crewmate.id == self.imposter.id:
                self.crewmatesAlive = True
        if self.crewmatesAlive == False:
            self.imposter.speed = 1
            self.imposter.progress = -999
            self.imposter.destination = [-200, random.randrange(0,self.screen.height())]
            QTimer.singleShot(3000, self.removeDead)

        #remove crewmates that don't exist
        for i in range(len(self.crewmates)):
            if not self.crewmates[i].exists == True:
                self.crewmates.pop(i)
                break

        #check if anybody has discovered bodies
        for i in self.crewmates:
            for j in self.crewmates:
                cautionDistance = (self.numCrewmates - len(self.crewmates) + 2) * 100
                if abs(i.x - j.x) < cautionDistance and abs(i.y - j.y) < cautionDistance:
                    if i.dead == True and j.dead == False and self.meeting == False and not j.id == self.imposter.id:
                        j.destination = [i.x, i.y]
                if abs(i.x - j.x) < 100 and abs(i.y - j.y) < 100:
                    if i.dead == True and j.dead == False and self.meeting == False and not j.id == self.imposter.id:
                        self.meeting = True
                        self.meetingLocation = [i.x, i.y]
                        self.sus = None
                        QTimer.singleShot(7000, self.removeSus)
                        QTimer.singleShot(10500, self.removeDead)
                        QTimer.singleShot(11000, self.endMeeting)

        #meeting logic
        if self.meeting == True:
            for i in range(len(self.crewmates)):
                #if self.imposter.cooldown > 29.5 * 60:
                #    if self.imposter.id == self.crewmates[i].id:
                #        self.sus = i
                crewmatesort = self.crewmates[:]
                crewmatesort.sort(key=lambda x: x.id, reverse=False)
                crewmate = crewmatesort[i]
                if crewmate.dead == False:
                    crewmate.activity = "meeting"
                    crewmate.progress = 0
                    crewmate.destination = [self.meetingLocation[0] + 100 * math.cos(i * (2 * math.pi / len(self.crewmates))),
                                            self.meetingLocation[1] + 100 * math.sin(i * (2 * math.pi / len(self.crewmates)))]
                    crewmate.speed = 0.5

        QTimer.singleShot(100, self.shipCycle)

    def removeDead(self):

        for crewmate in self.crewmates:
            if crewmate.dead == True:
                crewmate.delete()

    def endMeeting(self):
        for crewmate in self.crewmates:

            QTimer.singleShot(2500, crewmate.setSpeed)

            crewmate.destination = [random.randrange(0,self.screen.width()),
                                    random.randrange(0,self.screen.height())]

        self.meeting = False

    def removeSus(self):
        if self.sus == None:
            self.sus = random.randrange(0,len(self.crewmates))

        if self.crewmates[self.sus].dead == False:
            for crewmate in self.crewmates:
                if crewmate.dead == False:
                    crewmate.dx = -(crewmate.x - self.crewmates[self.sus].x) / 5
                    crewmate.dy = -(crewmate.y - self.crewmates[self.sus].y) / 5
                    QTimer.singleShot(50, self.crewmates[self.sus].die)

    def restart(self):
        for crewmate in self.crewmates:
            crewmate.delete()
        self.__init__(self.numCrewmates, self.display)
