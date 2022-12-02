try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from Buttons import *
from readingInputs import *


def preferencesScreen_onScreenStart(app):
    app.settingDict = eval(readFile("userPreferences.txt"))
    app.settings = []

def preferencesScreen_redrawAll(app):
    rectBottom = len(app.msgs)*20
    drawRect(20, 60,app.width -40, rectBottom, fill = rgb(217, 231, 241))

    for index in range(len(app.msgs)):
        msg = app.msgs[index]
        y = index*20 +70
        lastY =y
        drawLabel(msg, 20, y, size =16, fill = rgb(175, 125, 119), align = 'left')
    
def preferencesScreen_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('mainScreen')


def testFunction():
    strDict = str({'background': None, 'emptyCell': None, "initialVals":'black'})
    newDict = eval(strDict)
    settingDict = eval(readFile("userPreferences.txt"))
    print(settingDict['emptyCell'])
testFunction()
