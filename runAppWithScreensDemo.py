# runAppWithScreensDemo1.py
# This version only works in the sandbox, and not on the desktop.

from cmu_graphics import *

##################################
# Screen1
##################################

def screen1_onScreenStart(app):
    app.color = 'gold'

def screen1_onKeyPress(app, key):
    if key == 's': setActiveScreen('screen2')
    elif key == 'c': app.color = 'navy' if (app.color == 'gold') else 'gold'

def screen1_redrawAll(app):
    drawLabel('Screen 1', app.width/2, 30, size=16)
    drawLabel('Press c to change square color', app.width/2, 50, size=16)
    drawLabel('Press s to change screen to screen2', app.width/2, 70, size=16)
    drawRect(100, 100, app.width-200, app.height-200, fill=app.color)

##################################
# Screen2
##################################

def screen2_onScreenStart(app):
    app.cx = app.width/2
    app.dx = 10

def screen2_onKeyPress(app, key):
    if key == 's': setActiveScreen('screen1')
    elif key == 'd': app.dx = -app.dx

def screen2_onStep(app):
    app.cx = (app.cx + app.dx) % app.width

def screen2_redrawAll(app):
    drawLabel('Screen 2', app.width/2, 30, size=16)
    drawLabel('Press d to change direction of dot', app.width/2, 50, size=16)
    drawLabel('Press s to change the screen to screen1', app.width/2, 70, size=16)
    drawCircle(app.cx, app.height/2, 50, fill='lightGreen')

##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen='screen1', width=800)
