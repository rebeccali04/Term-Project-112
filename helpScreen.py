try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from Buttons import *


def helpScreen_onScreenStart(app):
    app.msgs =[]
    setAllMsgs(app)

def helpScreen_redrawAll(app):
    rectBottom = len(app.msgs)*20
    drawRect(20, 60,app.width -40, rectBottom, fill = rgb(217, 231, 241))

    for index in range(len(app.msgs)):
        msg = app.msgs[index]
        y = index*20 +70
        lastY =y
        drawLabel(msg, 20, y, size =16, fill = rgb(175, 125, 119), align = 'left')
    
def helpScreen_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('mainScreen')

def setMsg(app,msg):
    app.msgs.append(msg)

def setAllMsgs(app):
    allMsg = '''
Goal of the game: get all rows, column, boxes, 
filled with numbers 1-9 no duplicate in each region

press s for singleton (only in medium or harder modes)
press k for keyboard only mode
press button for mouse only mode
press n for normal mode/standard mode
press h for help
press space to go back
to set or remove a legal with keyboard hold L and your number
press space to go back to main screen or go to play screen from main screen
press 'a' or auto/manual button to toggle manual and auto legals
on graphics input screen put a 0 to erase input
press m for mouse only mode
press k for keyboard only mode
press n for normal mode
press space to go back to main screen

    '''
    for line in allMsg.splitlines():
        if line !='\n':
            setMsg(app, line)