try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
# from  import *
##################################
# mainScreen
##################################

def mainScreen_onScreenStart(app):
    app.color = 'gold'

def mainScreen_onKeyPress(app, key):
    if key == 'space': setActiveScreen('boardScreen')


def mainScreen_redrawAll(app):
    drawButton1('testing', 100,100,)


