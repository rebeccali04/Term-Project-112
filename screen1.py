try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *

##################################
# Screen1
##################################

def screen1_onScreenStart(app):
    app.color = 'gold'

def screen1_onKeyPress(app, key):
    if key == 's': setActiveScreen('boardScreen')
    elif key == 'c': app.color = 'navy' if (app.color == 'gold') else 'gold'

def screen1_redrawAll(app):
    drawLabel('Screen 1', app.width/2, 30, size=16)
    drawLabel('Press c to change square color', app.width/2, 50, size=16)
    drawLabel('Press s to change screen to screen2', app.width/2, 70, size=16)
    drawRect(100, 100, app.width-200, app.height-200, fill=app.color)
