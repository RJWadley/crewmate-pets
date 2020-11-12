import sys
import os
import random
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import QMainWindow, QMenu
from colors import *
from crewmate import Crewmate


class Imposter(Crewmate):
    def __init__(self, crewmates, *args, **kwargs):
        self.crewmates = crewmates
        self.cooldown = 0
        self.target = None
        super(Imposter, self).__init__(*args, **kwargs)
        print("success")

    def update(self):

        #activity manager
        if self.progress >= 120: #only choose a new activity every 2 seconds
            if not (self.activity == "beamIn"):
                randomNum = random.randrange(0,5)
                if randomNum == 0: #walk somewhere
                    self.activity = "wander"
                elif randomNum == 1: # stand idle
                    self.activity = "idle"
                elif randomNum < 5: # follow a crewmate
                    self.activity = "follow"
                print(self.activity)

            #restart with some variation
            self.progress = random.randrange(-20, 20)

        if self.activity == "follow":
            minDistance = None
            for crewmate in self.crewmates:
                if not self.id == crewmate.id and crewmate.dead == False:
                    distance = (crewmate.x - self.x) ** 2 + (crewmate.y - self.y) ** 2
                    if minDistance == None:
                        minDistance = distance
                        self.destination = [crewmate.x, crewmate.y]
                        self.target = crewmate.id
                    elif distance < minDistance:
                        minDistance = distance
                        self.destination = [crewmate.x, crewmate.y]
                        self.target = crewmate.id
            if not minDistance == None:
                if minDistance > 50 ** 2:
                    self.target = None
                if minDistance < 100 ** 2:
                    self.destination = [self.x, self.y]

        #kill logic
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.cooldown == 0 and not self.target == None:
            for crewmate in self.crewmates:
                if crewmate.id == self.target:
                    print("target:", crewmate.color)
                    distance = (crewmate.x - self.x) ** 2 + (crewmate.y - self.y) ** 2
                    if distance < 60 ** 2:
                        print("kill")
                        self.dx = (crewmate.x - self.x) * 2 / 10
                        self.dy = (crewmate.y - self.y) * 2 / 10
                        self.target = None;
                        self.activity = "idle"
                        self.cooldown = 600
                        QTimer.singleShot(100, crewmate.die)

                    else:
                        self.destination = [crewmate.x, crewmate.y]

        super(Imposter, self).update()

    def spriteLoop(self):

        if self.activity == "follow": #walk
            if abs(self.dx) > 0.1 or abs(self.dy) > 0.1:
                if self.spriteCount >= 12:
                    self.spriteCount = 0
                self.pixmap = self.walk[self.spriteCount]
                self.spriteCount += 1
            else:
                self.pixmap = self.idle

        super(Imposter, self).spriteLoop()
