try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from Buttons import *
##################################
# mainScreen
##################################

def mainScreen_onScreenStart(app):
    app.mainScreenButtons = [] #(msg, top, left, length, height, hover)
    setAllButtons(app)
    app.currMode = 'easy'

def mainScreen_onKeyPress(app, key):
    if key == 'space': 
        # app.currScreen = 'boardScreen'
        setActiveScreen('boardScreen')

def mainScreen_redrawAll(app):
    drawTitle(app, "SUDOKU",)
    drawAllButtons(app.mainScreenButtons)

def drawTitle(app, msg, size =40):
    centerX = app.width/2
    drawLabel(msg, centerX, 150, size = size, bold = True, fill = rgb(196, 156, 145))

def mainScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.mainScreenButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.mainScreenButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.mainScreenButtons)

def mainScreen_onMousePress(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.mainScreenButtons, mouseX, mouseY)
    if buttonClickedIndex ==0:
        # app.currScrren = 'boardScreen'
        setActiveScreen('boardScreen')
    elif buttonClickedIndex ==1:
        #Mode
        setActiveScreen('modeScreen')
    elif buttonClickedIndex ==2:
        setActiveScreen('inputBoardScreen')
        print('input board')
    elif buttonClickedIndex ==3:
        setActiveScreen('helpScreen')
        print('how to play')

#for main screen
def setAllButtons(app):
    centerX = app.width/2 - 150/2
    startY = 225
    setButton(app.mainScreenButtons, 'Play',centerX , startY,)
    setButton(app.mainScreenButtons, 'Mode', centerX, startY+80*1,)
    setButton(app.mainScreenButtons, 'Input Board', centerX, startY+80*2,)
    setButton(app.mainScreenButtons, 'How to Play', centerX, startY+80*3,)



########TESTING OTHER SCREENS##################################

#for modeScreen
# def setAllButtons(app):
#     centerX = app.width/2 - 150/2
#     startY = 225
#     setButton(app.mainScreenButtons, 'EASY',centerX , startY,)
#     setButton(app.mainScreenButtons, 'MEDIUM', centerX, startY+80*1,)
#     setButton(app.mainScreenButtons, 'HARD', centerX, startY+80*2,)
#     setButton(app.mainScreenButtons, 'EXPERT', centerX, startY+80*3,)
#     setButton(app.mainScreenButtons, 'EVIL', centerX, startY+80*4,)
#     setButton(app.mainScreenButtons, 'Back',50 , 40, length =60, height =40)
