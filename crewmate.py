import sys
import os
import random
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import QMainWindow, QApplication, QMenu
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
        #random position
        self.x = random.randrange(0,self.screen.width() - self.width)
        self.y = random.randrange(0,self.screen.height() - self.height)
        self.dx = 0
        self.dy = 0
        #speed is low by default because otherwise it gets crazy
        self.speed = 0.1
        #random destination
        self.destination = (random.randrange(0,self.screen.width() - self.width), random.randrange(0,self.screen.height() - self.height))
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
        self.move(round(self.x), round(self.y))

    def loadImages(self):

        #create QImage and color it
        idle = os.path.join('img', 'default','idle.png')
        self.idle = QImage(idle)
        self.idle = toColor(self.idle, self.color)
        #then convert to pixmap in place
        self.idle = QPixmap.fromImage(self.idle)

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
            self.draggingPos = event.globalPos() - self.pos()
            #keeping a running average to prevent flick back
            self.dxArray = []
            self.dyArray = []
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.dragging == True:

            self.activity = "idle" #set sprite to idle for now
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
            self.destination = (self.x, self.y) # prevent movement

        if self.activity == "idle": #idle
            self.pixmap = self.idle

        if self.activity == "walk": #walk
            if self.spriteCount >= 12:
                self.spriteCount = 0
            self.pixmap = self.walk[self.spriteCount]
            self.spriteCount += 1

        #flip when moving left
        if self.dx < 0:
            self.pixmap = self.pixmap.transformed(QTransform().scale(-1, 1))

        #redraw sprite before loop
        self.repaint()
        QTimer.singleShot(50, self.spriteLoop)

    def update(self):

        #activity manager
        if self.progress >= 30: #only choose a new activity 2x per second
            self.progress = 1
            if not (self.activity == "beamIn"):
                randomNum = random.randrange(0,2)
                if randomNum == 1: #walk somewhere
                    self.activity = "walk"
                    if (abs(self.destination[0] - self.x) < 50) and (abs(self.destination[1] - self.y) < 50):
                        self.destination = (random.randrange(0,self.screen.width() - self.width), random.randrange(0,self.screen.height() - self.height))

                elif randomNum == 0: # stand idle
                    self.activity = "idle"
                    self.destination = (self.x, self.y)

        self.progress += 1

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

        self.move(round(self.x), round(self.y))

        QTimer.singleShot(16, self.update)

    def contextMenuEvent(self, e):

        menu = QMenu(self)

        close = menu.addAction("~delete crewmate~")
        close.triggered.connect(self.delete)

        close = menu.addAction("~delete all crewmates~")
        close.triggered.connect(sys.exit)

        menu.exec_(e.globalPos())
        self.contenting = True

    def delete(self):
        self.exists = False
        self.close()
