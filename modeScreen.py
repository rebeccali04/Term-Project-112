try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from Buttons import *


def modeScreen_onScreenStart(app):
    print('startingModeScreen')
    app.cx = app.width/2
    app.dx = 10

def modeScreen_onKeyPress(app, key):
    if key == 's': setActiveScreen('screen1')
    elif key == 'd': app.dx = -app.dx

def modeScreen_onStep(app):
    app.cx = (app.cx + app.dx) % app.width


def modeScreen_redrawAll(app):
    drawLabel('Screen 2', app.width/2, 30, size=16)
    drawLabel('Press d to change direction of dot', app.width/2, 50, size=16)
    drawLabel('Press s to change the screen to screen1', app.width/2, 70, size=16)
    drawCircle(app.cx, app.height/2, 50, fill='lightGreen')
    