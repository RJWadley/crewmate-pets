import tkinter as tk
from tkinter import *
import os
import PIL.Image
import PIL.ImageTk
import random

x = 100
y = 100
SCREEN = (1366, 768)
imgholder = 0

class Crewmate:
    def __init__(self, root):
        #definitions
        self.x = random.randrange(0,SCREEN[0])
        self.y = random.randrange(0,SCREEN[1])
        self.dx = 0
        self.dy = 0
        self.master = Toplevel()
        self.width = 100
        self.height = 100
        self.speed = 0.1
        self.destination = (100,100)
        self.progress = 0

        #static image
        print('init')
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'img', 'default','idle.png')
        preimg = PIL.Image.open(filename)
        img1 = PIL.ImageTk.PhotoImage(preimg)
        self.img1 = img1

        self.label = tk.Label(self.master, image=img1, bg='white')
        self.label.pack()

        self.canvas = Canvas(self.master, width=self.width, height=self.height, bd=-2, bg='yellow')
        self.canvas.pack()

        self.canvas.create_image(self.width/2, self.height/2, image=img1)

        self.master.overrideredirect(True)
        self.master.wm_attributes("-topmost", True)
        #self.master.wm_attributes("-transparentcolor", "yellow")
        self.master.geometry(str(self.width) + 'x' + str(self.height) + '+-1000+-1000')

        self.master.after(100, self.update)

    def update(self):

        if self.progress >= 60:
            self.progress = 1
            activity = random.randrange(1,5)
            if activity == 1: #walk somewhere
                self.destination = (random.randrange(0,SCREEN[0]), random.randrange(0,SCREEN[1]))
                print("walk")
            elif activity == 2:
                self.destination = (self.x, self.y)
                print("stand")

        self.progress += 1

        self.master.geometry(str(self.width) + 'x' + str(self.height) + '+'+str(round(self.x))+'+'+str(round(self.y)))
        self.master.after(16, self.update)

        if (abs(self.destination[0] - self.x) < 10) and (abs(self.destination[1] - self.y) < 10):
            dx = 0
            dy = 0

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

# this is the main/root window
root = tk.Tk()
root.title("Window 1")
root.wm_attributes("-topmost", True)
leaveButton = tk.Button(root, text="Quit", command=root.destroy)
leaveButton.grid(row=1, column=1, sticky='nw')
#root.withdraw()
root.after(1000, root.deiconify)

steve1 = Crewmate(root)
steve2 = Crewmate(root)
root.mainloop()
