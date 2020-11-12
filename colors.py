
from PySide2.QtGui import *
from PySide2.QtCore import *
import colorsys

def toColor(im, color):

    alpha = im.alphaChannel()

    if color == "Lime":
        hue = 113
    if color == "Red":
        hue = 360
    if color == "Orange":
        hue = 30;
    if color == "Yellow":
        hue = 60;
    if color == "Cyan":
        hue = 188
    if color == "Purple":
        hue = 263
    if color == "Pink":
        hue = 310
    if color == "Blue":
        hue = 231

    for x in range(im.width()):
        for y in range(im.height()):
            r, g, b, a = QColor(im.pixel(x ,y)).getRgb()
            if (abs(r - g) < 5 and abs(g - b) < 5):
                pass
            elif (g >= 100):
                r, g, b = colorsys.hsv_to_rgb(195/360, 32/100, round(g * 0.9)/255)
                r *= 255
                g *= 255
                b *= 255
            elif (r >= 100):
                r, g, b = colorsys.hsv_to_rgb(hue/360, 91/100, 90/100)
                r *= 255
                g *= 255
                b *= 255
            elif (b >= 100):
                r, g, b = colorsys.hsv_to_rgb(hue/360, 94/100, 60/100)
                r *= 255
                g *= 255
                b *= 255
            else:
                pass
            # ... do something to r, g, b, a ...
            im.setPixel(x, y, QColor(r, g, b, a).rgb())


    #make shadow trans
    for x in range(im.width()):
        for y in range(im.height()):
            r, g, b, a = QColor(im.pixel(x ,y)).getRgb()
            SHADOW_TOLERANCE = 5
            if (abs(r - 55) <= SHADOW_TOLERANCE and abs(g - 59) <= SHADOW_TOLERANCE and abs(b - 60) <= SHADOW_TOLERANCE):
                alpha.setPixel(x, y, 100)

    im.setAlphaChannel(alpha);

    return im
