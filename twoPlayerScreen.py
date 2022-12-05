try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from boardScreen import *
from runAppWithScreens import *
from Buttons import *

def twoPlayerScreen_onScreenStart(app):
    pass

def twoPlayerScreen_redrawAll(app):
    redrawBoardScreen(app)

def twoPlayerScreen_onKeyPress(app, key):
    if not app.competitionMode:
        if key == 'o':
            highlightHint(app)
        elif key == 'p':
            doHint(app)
        if key =='s' and app.currMode != 'easy':
            #play singleton
            app.state.playHint1()
    if key =='u':
        app.state = app.state.undo()
    if key == 'r':
        app.state = app.state.redo()
    if key == 'h':
        print('help')
        setActiveScreen('helpScreen')

    if key =='m':
        app.currInputMode = 'mouse'
    elif key =='n':
        app.currInputMode = 'normal'
    elif key == 'k':
        app.currInputMode = 'key'
    if app.currInputMode != 'mouse':
        if key == 'space': setActiveScreen('mainScreen')
        if key == 'backspace' or key == '0':
            app.state.undoSet(*app.selectedCell, app.prevStepLegals)
        elif key.isdigit(): #not including 0
            num =int(key)
            doInputNum(app, num)
        
        if key =='l':
            app.inputingLegals =True
        if key =='a': 
            app.usingAutoLegals =not app.usingAutoLegals
        
        #up down left right
        
        if key == 'left':    moveSelection(app, 0, -1)
        elif key == 'right': moveSelection(app, 0, +1)
        elif key == 'up':    moveSelection(app ,-1, 0)
        elif key == 'down':  moveSelection(app, +1, 0) 
    #modified, from https://cs3-112-f22.academy.cs.cmu.edu/notes/4189


def twoPlayerScreen_onKeyRelease(app, key):
    if key =='l':
        app.inputingLegals =False

def twoPlayerScreen_onMousePress(app,mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
      if selectedCell != app.selectedCell:
        app.selectedCell = selectedCell
    buttonClickedIndex = getButtonClicked(app.boardScreenButtons, mouseX, mouseY)
    if buttonClickedIndex ==0:
        setActiveScreen('mainScreen')
    elif buttonClickedIndex ==1 and app.currMode != 'easy' and not app.competitionMode:
        app.state.playHint1()
    elif buttonClickedIndex ==2:
        restartBoardScreen(app)
        print('New Game')
    elif buttonClickedIndex ==3:
        app.usingAutoLegals = not app.usingAutoLegals 

    if app.currInputMode == 'mouse':
        #check for numPad
        numPadCell = getNumPadCell(app, mouseX, mouseY)
        if numPadCell!=None:
            if numPadCell == 0:
                print('toggle setting legals') #add setting candidate toggle
                app.inputingLegals = not app.inputingLegals
            else:
                doInputNum(app, numPadCell)


def twoPlayerScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.boardScreenButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.boardScreenButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.boardScreenButtons)