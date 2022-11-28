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
    


def setMsg(app,msg):
    app.msgs.append(msg)

def setAllMsgs(app):
    allMsg = '''
press s for singleton
press k for keyboard only mode
press button for mouse only mode
press n for normal mode/standard mode
press h for help
press space to go back
to set or remove a legal with keyboard hold l and your number
press legals to toggle auto and manual legals
press space to go back to main screen or go to play screen from main screen
press a to toggle manual and auto legals
on graphics input screen put a 0 to erase input
press m for mouse only mode
press k for keyboard only mode
press n for normal mode
    '''
    for line in allMsg.splitlines():
        if line !='\n':
            setMsg(app, line)