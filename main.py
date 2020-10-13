import sys
import os
import random
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import QMainWindow, QApplication, QMenu
from colors import *

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MainWindow(QMainWindow):

    def __init__(self, color, id):

        self.id = id
        self.color = color
        self.width = 200
        self.height = 200
        self.x = random.randrange(0,screen.width() - self.width)
        self.y = random.randrange(0,screen.height() - self.height)
        self.dx = 0
        self.dy = 0
        self.speed = 0.1
        self.destination = (random.randrange(0,screen.width() - self.width), random.randrange(0,screen.height() - self.height))
        self.progress = 0
        self.activity = "beamIn"
        self.spriteCount = 0
        self.exists = False
        self.dxArray = []
        self.dyArray = []
        self.dragging = False

        self.loadImages()
        self.initUI()
        self.spriteLoop()
        QTimer.singleShot(1, self.update)
        QTimer.singleShot(1000, self.exist)

    def exist(self):
        self.exists = True

    def initUI(self):

        super(MainWindow, self).__init__()
        self.title = "Crewmate"
        self.setWindowTitle(self.title)

        #make transparent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(self.width, self.height)
        self.move(round(self.x), round(self.y))

    def loadImages(self):

        filename = os.path.join('img', 'default','idle.png')

        self.idle = QImage(filename)
        self.idle = toColor(self.idle, self.color)

        self.idle = QPixmap.fromImage(self.idle)
        self.pixmap = self.idle
        pixmap = self.idle

        self.walk = []
        for i in range(12):
            filename = os.path.join('img', 'default','walk','walkcolor' + str(i+1).zfill(4) + '.png')
            pixmap = QImage(filename)
            pixmap = toColor(pixmap, self.color)
            pixmap = QPixmap.fromImage(pixmap)
            print("loaded", filename, "for crewmate", self.id)
            self.walk.append(pixmap)

        self.beamIn = []
        for i in range(52):
            filename = os.path.join('img', 'default','spawn','spawn' + str(i+1).zfill(4) + '.png')
            pixmap = QImage(filename)
            if i >= 32:
                pixmap = toColor(pixmap, self.color)
            pixmap = QPixmap.fromImage(pixmap)
            print("loaded", filename, "for crewmate", self.id)
            self.beamIn.append(pixmap)

    def paintEvent(self, pixmap):
        qp = QPainter()
        qp.begin(self)

        qp.drawPixmap(self.width / 2 - self.pixmap.width() / 2, self.height - self.pixmap.height(), self.pixmap)

        qp.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.draggingPos = event.globalPos() - self.pos()
            self.dxArray = []
            self.dyArray = []
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.dragging == True:

            self.activity = "idle"
            self.dxArray.append((event.globalPos() - self.draggingPos).x() - self.x)
            self.dyArray.append((event.globalPos() - self.draggingPos).y() - self.y)
            if len(self.dxArray) > 30:
                self.dxArray.pop(0)
            if len(self.dyArray) > 30:
                self.dyArray.pop(0)
            self.dx = sum(self.dxArray) / len(self.dxArray) * 2
            self.dy = sum(self.dyArray) / len(self.dyArray) * 2
            self.x = (event.globalPos() - self.draggingPos).x()
            self.y = (event.globalPos() - self.draggingPos).y()

    def spriteLoop(self):

        if self.exists == False:
            QTimer.singleShot(1000, self.spriteLoop)
            return

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

        if self.dx < 0:
            self.pixmap = self.pixmap.transformed(QTransform().scale(-1, 1))

        self.repaint()

        QTimer.singleShot(50, self.spriteLoop)

    def update(self):

        if self.exists == False:
            QTimer.singleShot(1000, self.update)
            return

        #activity manager
        if self.progress >= 30:
            self.progress = 1
            if not (self.activity == "beamIn"):
                randomNum = random.randrange(0,2)
                if randomNum == 1: #walk somewhere
                    self.activity = "walk"
                    if (abs(self.destination[0] - self.x) < 50) and (abs(self.destination[1] - self.y) < 50):
                        self.destination = (random.randrange(0,screen.width() - self.width), random.randrange(0,screen.height() - self.height))

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
        for i in range(len(crewmates)):
            if crewmates[i].id == self.id:
                crewmates.pop(i)
                return

app = QApplication(sys.argv)

display = app.primaryScreen()
screen = display.size()

crewmates = []
colors = ["Lime", "Red", "Cyan", "Orange", "Yellow"]

def ship():

    crewmatesort = crewmates[:]
    crewmatesort.sort(key=lambda x: x.y, reverse=False)
    if not (crewmatesort == crewmates):
        crewmates.sort(key=lambda x: x.y, reverse=False)
        for crewmate in crewmates:
            crewmate.raise_()

    if len(crewmates) == 0:
        sys.exit()

    QTimer.singleShot(16, ship)

def init():
    for i in range(5):
        crewmate = MainWindow(colors[i], i)
        crewmates.append(crewmate)
        crewmate.show()

    ship()

init()

sys.exit(app.exec_())
