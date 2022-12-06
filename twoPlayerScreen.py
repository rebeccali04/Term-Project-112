try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from boardScreen import *
from runAppWithScreens import *
from Buttons import *

def twoPlayerScreen_onScreenStart(app):
    app.gamePaused = True #should be True in the begining
    app.twoPlayerButtons = []
    setButton(app.twoPlayerButtons, 'Start', 550, 40, length =60, height =40)
    restartGame(app)
    
def restartGame(app):
    app.twoPlayerMsg = ''
    app.turn = 1 # 1 or 2
    app.player1Scores = 0
    app.player2Scores = 0
    

def twoPlayerScreen_redrawAll(app):
    redrawBoardScreen(app)
    drawTwoPlayerStats(app)
    drawAllButtons(app.twoPlayerButtons)


def twoPlayerScreen_onKeyPress(app, key):
    boardScreenKeyPress(app, key) 
    

def twoPlayerScreen_onMousePress(app,mouseX,mouseY):
    boardScreenDoMousePress(app,mouseX,mouseY)
    #for two player specific
    buttonClickedIndex = getButtonClicked(app.twoPlayerButtons, mouseX, mouseY)
    if buttonClickedIndex == 0:
        app.gamePaused = not app.gamePaused
        if app.gamePaused:
            app.twoPlayerButtons[0]['msg'] = 'Start'
        else:
            app.twoPlayerButtons[0]['msg'] = 'Pause'

def twoPlayerScreen_onMouseMove(app, mouseX, mouseY):
    boardScreenMouseMove(app,mouseX,mouseY)
    buttonClickedIndex = getButtonClicked(app.twoPlayerButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.twoPlayerButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.twoPlayerButtons)

def drawTwoPlayerStats(app):
    drawRect(600, 200, 100,200, fill = None)
    pass
