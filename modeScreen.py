try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from Buttons import *
from State import *
from boardScreen import *
##################################
# mainScreen
##################################

def modeScreen_onScreenStart(app):
    app.modeScreenButtons = [] #(msg, top, left, length, height, hover)
    setAllButtons(app)

def modeScreen_onKeyPress(app, key):
    print('this is the mode screen key press')
    if key == 'space': 
        # app.currScreen = 'boardScreen'
        setActiveScreen('mainScreen')

def modeScreen_redrawAll(app):
    drawTitle(app, "Mode Selection",)
    drawAllButtons(app.modeScreenButtons)
    drawLabel(f'Your current mode is {app.currMode.upper()}', app.width/2, 200, size =14)

def modeScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.modeScreenButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.modeScreenButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.modeScreenButtons)

def drawTitle(app, msg, size =40):
    centerX = app.width/2
    drawLabel(msg, centerX, 150, size = size, bold = True, fill = rgb(196, 156, 145))

def modeScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.modeScreenButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.modeScreenButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.modeScreenButtons)

def modeScreen_onMousePress(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.modeScreenButtons, mouseX, mouseY)
    prevMode = app.currMode
    if buttonClickedIndex ==0:
        # Easy
        app.currMode = 'easy'
    elif buttonClickedIndex ==1:
        #Medium
        app.currMode = 'medium'
    elif buttonClickedIndex ==2:
        #hard
        app.currMode = 'hard'
    elif buttonClickedIndex ==3:
        #Expert
        app.currMode = 'expert'
    elif buttonClickedIndex ==4:
        #evil
        app.currMode = 'evil'
    elif buttonClickedIndex ==5:
        #back
        setActiveScreen('mainScreen')
    #was changed load new board
    if app.currMode != prevMode:
        restartBoardScreen(app)

#for main screen
def setAllButtons(app):
    centerX = app.width/2 - 150/2
    startY = 225
    setButton(app.modeScreenButtons, 'EASY',centerX , startY,)
    setButton(app.modeScreenButtons, 'MEDIUM', centerX, startY+80*1,)
    setButton(app.modeScreenButtons, 'HARD', centerX, startY+80*2,)
    setButton(app.modeScreenButtons, 'EXPERT', centerX, startY+80*3,)
    setButton(app.modeScreenButtons, 'EVIL', centerX, startY+80*4,)
    setButton(app.modeScreenButtons, 'Back',50 , 40, length =60, height =40)
