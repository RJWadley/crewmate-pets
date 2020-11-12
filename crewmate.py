import sys
import os
import random
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import QMainWindow, QMenu
from colors import *

# for getting images
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Crewmate(QMainWindow):

    def __init__(self, color, id, screen):
        self.screen = screen #display size
        self.id = id
        self.color = color
        self.width = 200
        self.height = 200
        self.dead = False
        self.meeting = False
        #random position
        self.x = random.randrange(0,self.screen.width() - self.width)
        self.y = random.randrange(0,self.screen.height() - self.height)
        self.dx = 0
        self.dy = 0
        #speed is low by default because otherwise it gets crazy
        self.setSpeed()

        #random destination
        self.destination = [random.randrange(0,self.screen.width() - self.width),
                            random.randrange(0,self.screen.height() - self.height)]
        self.zoneSize = 200
        self.edgeBuffer = 50
        #sprite stuff
        self.progress = 0
        self.activity = "beamIn"
        self.spriteCount = 0
        self.exists = True
        #dragging stuff
        self.dxArray = []
        self.dyArray = []
        self.dragging = False

        #load and start loops
        self.loadImages()
        self.initUI()
        self.spriteLoop()
        QTimer.singleShot(1, self.update)

    def setSpeed(self):
        self.speed = 0.1

    def initUI(self):

        #create window
        super(Crewmate, self).__init__()
        self.title = "Crewmate"
        self.setWindowTitle(self.title)

        #make transparent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        #sizing and placement
        self.resize(self.width, self.height)
        self.move(round(self.x - self.width / 2), round(self.y - self.height))

    def loadImages(self):

        #create QImage and color it
        idle = os.path.join('img', 'default','idle.png')
        self.idle = QImage(idle)
        self.idle = toColor(self.idle, self.color)
        #then convert to pixmap in place
        self.idle = QPixmap.fromImage(self.idle)

        #create QImage and color it
        idle = os.path.join('img', 'default','ejected.png')
        self.ejected = QImage(idle)
        self.ejected = toColor(self.ejected, self.color)
        #then convert to pixmap in place
        self.ejected = QPixmap.fromImage(self.ejected)

        #sprite loop for walking
        self.walk = []
        for i in range(12):
            #create QImage, color it, convert to pixmap, append
            filename = os.path.join('img', 'default','walk','walkcolor' + str(i+1).zfill(4) + '.png')
            pixmap = QImage(filename)
            pixmap = toColor(pixmap, self.color)
            pixmap = QPixmap.fromImage(pixmap)
            print("loaded", filename, "for crewmate", self.id)
            self.walk.append(pixmap)

        #sprite loop for beam in animation
        self.beamIn = []
        for i in range(52):
            #create QImage, color it, convert to pixmap, append
            filename = os.path.join('img', 'default','spawn','spawn' + str(i+1).zfill(4) + '.png')
            pixmap = QImage(filename)
            #only color ones that aren't pure white
            if i >= 32:
                pixmap = toColor(pixmap, self.color)
            pixmap = QPixmap.fromImage(pixmap)
            print("loaded", filename, "for crewmate", self.id)
            self.beamIn.append(pixmap)

        #sprite loop for death
        self.deathSprite = []
        for i in range(40):
            #create QImage, color it, convert to pixmap, append
            filename = os.path.join('img', 'default','dead','Dead' + str(i+1).zfill(4) + '.png')
            pixmap = QImage(filename)
            pixmap = toColor(pixmap, self.color)
            pixmap = QPixmap.fromImage(pixmap)
            print("loaded", filename, "for crewmate", self.id)
            self.deathSprite.append(pixmap)

        #set first pixmap to beginning of beamIn
        self.pixmap = self.beamIn[0]

    def paintEvent(self, pixmap):
        qp = QPainter()
        qp.begin(self)
        #center at bottom middle of window
        qp.drawPixmap(self.width / 2 - self.pixmap.width() / 2, self.height - self.pixmap.height(), self.pixmap)
        qp.end()

    def mousePressEvent(self, event):
        #dragging
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.draggingPos = event.globalPos() - self.pos() - QPoint(self.width / 2, self.height)
            #keeping a running average to prevent flick back
            self.dxArray = []
            self.dyArray = []
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.activity = "idle"

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.dragging == True:

            if self.dead == False:
                self.activity = "dragging"
            #keep a running average
            self.dxArray.append((event.globalPos() - self.draggingPos).x() - self.x)
            self.dyArray.append((event.globalPos() - self.draggingPos).y() - self.y)
            #cap average total at 30
            if len(self.dxArray) > 30:
                self.dxArray.pop(0)
            if len(self.dyArray) > 30:
                self.dyArray.pop(0)
            #set velocity to current average
            self.dx = sum(self.dxArray) / len(self.dxArray) * 2
            self.dy = sum(self.dyArray) / len(self.dyArray) * 2
            #ensure position is where mouse is
            self.x = (event.globalPos() - self.draggingPos).x()
            self.y = (event.globalPos() - self.draggingPos).y()

    def spriteLoop(self):

        if self.activity == "beamIn":
            if self.spriteCount >= 52:
                self.spriteCount = 0
                self.activity = "idle"
            self.pixmap = self.beamIn[self.spriteCount]
            self.spriteCount += 1
            self.destination = [self.x, self.y] # prevent movement

        elif self.activity == "die":
            self.pixmap = self.deathSprite[self.spriteCount]
            self.spriteCount += 1
            if self.spriteCount >= 40:
                self.spriteCount = 39

        elif self.activity == "dragging":
            self.pixmap = self.ejected

        elif abs(self.dx) > 0.2 or abs(self.dy) > 0.2:
            if self.spriteCount >= 12:
                self.spriteCount = 0
            self.pixmap = self.walk[self.spriteCount]
            self.spriteCount += 1
        else:
            self.pixmap = self.idle

        #flip when moving left
        if self.dx < 0:
            self.pixmap = self.pixmap.transformed(QTransform().scale(-1, 1))

        #redraw sprite before loop
        self.repaint()
        QTimer.singleShot(50, self.spriteLoop)

    def update(self):

        if self.dead == False:
            #activity manager
            if self.progress >= 120: #only choose a new activity every 2 seconds
                if not (self.activity == "beamIn"):
                    randomNum = random.randrange(0,2)

                    if randomNum == 1: #walk somewhere
                        self.activity = "wander"
                    elif randomNum == 0: # stand idle
                        self.activity = "idle"

                #restart with some variation
                self.progress = random.randrange(-20, 20)

            self.progress += 1

            if self.activity == "wander":
                if (abs(self.destination[0] - self.x) < 10) and (abs(self.destination[1] - self.y) < 10):
                    for i in range(10):
                        #round position for randranges
                        self.x = round(self.x)
                        self.y = round(self.y)
                        self.destination = [random.randrange(round(self.x) - 300, round(self.x) + 300),
                                            random.randrange(round(self.y) - 300, round(self.y) + 300)]

                        if (self.destination[0] > self.edgeBuffer and self.destination[0] < self.zoneSize) or (self.destination[0] < self.screen.width() - self.edgeBuffer and self.destination[0] > self.screen.width() - self.zoneSize):
                            if (self.destination[1] > self.edgeBuffer + 100 and self.destination[1] + 100 < self.zoneSize) or (self.destination[1] < self.screen.height() - self.edgeBuffer and self.destination[1] > self.screen.height() - self.zoneSize):
                                break
                        else:
                            self.destination[0] = max(self.destination[0], self.edgeBuffer)
                            self.destination[1] = max(self.destination[1], self.edgeBuffer + 100)
                            self.destination[0] = min(self.destination[0], self.screen.width() - self.edgeBuffer)
                            self.destination[1] = min(self.destination[1], self.screen.height() - self.edgeBuffer)

            if self.activity == "idle":
                self.destination = [self.x, self.y]

        #movement
        if (abs(self.destination[0] - self.x) > 10):
            ddx = self.destination[0] - self.x
        else:
            ddx = 0
        if (abs(self.destination[1] - self.y) > 10):
            ddy = self.destination[1] - self.y
        else:
            ddy = 0

        while (abs(ddx) > self.speed) or (abs(ddy) > self.speed):
            ddx *= 0.9
            ddy *= 0.9

        self.dx += ddx
        self.dy += ddy

        self.x += self.dx
        self.y += self.dy
        self.dx *= 0.9
        self.dy *= 0.9

        self.move(round(self.x - self.width / 2), round(self.y - self.height))

        QTimer.singleShot(16, self.update)

    def die(self):
        if self.dead == False:
            self.dead = True;
            self.activity = "die"
            self.destination = [self.x, self.y]
            self.spriteCount = 0

    def contextMenuEvent(self, e):

        menu = QMenu(self)

        close = menu.addAction("~delete crewmate~")
        close.triggered.connect(self.delete)

        close = menu.addAction("~delete all crewmates~")
        close.triggered.connect(sys.exit)

        close = menu.addAction("~kill this crewmate~")
        close.triggered.connect(self.die)

        menu.exec_(e.globalPos())
        self.contenting = True

    def delete(self):
        self.exists = False
        self.close()
