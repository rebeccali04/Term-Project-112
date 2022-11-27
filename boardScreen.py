try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from State import *
import math
from readingInputs import *
from Buttons import *
##################################
# boardScreen
##################################

#Todo
# inputing numbers function

def boardScreen_onScreenStart(app):
    app.boardLeft = 100 #app.width*0.1
    app.boardTop = 100 #app.height*0.15
    boardSideLen = min(app.width*0.8,app.height*0.8)
    app.boardWidth = boardSideLen
    app.boardHeight = boardSideLen
    app.cellBorderWidth = 2
    app.lineColor = 'gray'
    app.boarderColor ='black'
    app.sectionBoxesColor = 'black'
    restartBoardScreen(app)

def restartBoardScreen(app):
    app.boardScreenButtons = []
    #load board
    board = loadRandomBoard(app.currMode)
    app.state = State(board)
    app.selectedCell = (0,0)
    app.inputingLegals =False
    setAllButtons(app)
    #move to mode
    if app.currMode == 'easy':
        app.usingAutoLegals = False
    else: 
        app.usingAutoLegals =True
    

def boardScreen_onKeyPress(app, key):
    if key == 'space': setActiveScreen('mainScreen')
    if key.isdigit():
        row,col = app.selectedCell
        val =int(key)
        if not app.state.cellInOriginalBoard(row,col):
            if app.inputingLegals: 
                if not app.usingAutoLegals:
                    app.state.inputLegals(row, col, val)
            else:
                app.state.set(row, col,val )
    if key =='s':
        #play singleton
        app.state.playHint1()
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

def moveSelection(app, drow, dcol):
    if app.selectedCell != None:
        selectedRow, selectedCol = app.selectedCell
        newSelectedRow = (selectedRow + drow) % app.state.rows
        newSelectedCol = (selectedCol + dcol) % app.state.cols
        app.selectedCell = (newSelectedRow, newSelectedCol)
#modified, from https://cs3-112-f22.academy.cs.cmu.edu/notes/4189


def boardScreen_onKeyRelease(app, key):
    if key =='l':
        app.inputingLegals =False

def boardScreen_onMousePress(app,mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
      if selectedCell != app.selectedCell:
        app.selectedCell = selectedCell
    buttonClickedIndex = getButtonClicked(app.boardScreenButtons, mouseX, mouseY)
    if buttonClickedIndex ==0:
        setActiveScreen('mainScreen')
    elif buttonClickedIndex ==1:
        print('Hint')
        app.state.playHint1()
    elif buttonClickedIndex ==2:
        restartBoardScreen(app)
        print('New Game')
    elif buttonClickedIndex ==3:
        app.usingAutoLegals = not app.usingAutoLegals 
        print('legals toggle')



def boardScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.boardScreenButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.boardScreenButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.boardScreenButtons)

def boardScreen_redrawAll(app):
    boardScreen_drawBoard(app)
    boardScreen_drawBoardBorder(app)
    boardScreen_DrawSectionBoxes(app)
    drawSudokuNumbers(app, app.state.userBoard)
    drawAllLegals(app)
    drawAllButtons(app.boardScreenButtons)
    
    ########################################################
    #                      Buttons                         #
    ########################################################

def setAllButtons(app):
    y = 40
    setButton(app.boardScreenButtons, 'Back',50 , y, length =60, height =40)
    setButton(app.boardScreenButtons, 'Singleton',125 , y,length =100, height =40)
    setButton(app.boardScreenButtons, 'New Game',250 , y,length =100, height =40)
    setButton(app.boardScreenButtons, 'Legals',375 , y,length =100, height =40)


    ########################################################
    #                      HELPERS                         #
    ########################################################

def drawSudokuNumbers(app, boardToDraw):
    cellWidth, cellHeight = getCellSize(app)
    for row in range(app.state.rows):
        for col in range(app.state.cols):
            color = rgb(175, 125, 119) if not app.state.cellInOriginalBoard(row,col) else 'black'
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellX = cellLeft+cellWidth/2
            cellY = cellTop +cellHeight/2
            num =boardToDraw[row][col]
            if num!=0:
                drawLabel(str(num),cellX, cellY, size = app.width//20, bold = True, fill =color)
                
def drawAllLegals(app):
    if app.usingAutoLegals:
        legals = app.state.legals
    else:
        legals = app.state.userLegals
    for row in range(app.state.rows):
        for col in range(app.state.cols):
            if app.state.userBoard[row][col]==0:
                legalsSet = legals[row][col]
                drawLegalsInCell(app, row, col, legalsSet)

def drawLegalsInCell(app, row, col, legalsSet):
    cellLeft, cellTop =getCellLeftTop(app, row, col)
    cellWidth, cellHeight =getCellSize(app)
    for num in range(1,10): #from 1 to 9
        if num in legalsSet:
            legalRow = (num-1)//3
            legalCol = (num-1)%3
            legalHeight =cellHeight/3
            legalWidth = cellWidth/3
            legalLeft = cellLeft + legalCol * legalHeight
            legalTop = cellTop + legalRow * legalWidth
            legalX = legalLeft + legalHeight/2
            legalY = legalTop + legalWidth/2 #from logic of drawSudokuNumbers and getCellleftTop
            
            drawLabel(str(num), legalX,legalY)
'''
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

    cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellX = cellLeft+cellWidth/2
            cellY = cellTop +cellHeight/2
'''
def boardScreen_drawBoard(app):
    for row in range(app.state.rows):
        for col in range(app.state.cols):
            boardScreen_drawCell(app, row, col)
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def boardScreen_drawBoardBorder(app):
  # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border=app.boarderColor,
           borderWidth=2*app.cellBorderWidth)
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def boardScreen_DrawSectionBoxes(app):
    for sectionRow in range(0,app.state.rows,3):
        for sectionCol in range(0,app.state.cols,3):
            cellLeft, cellTop = getCellLeftTop(app, sectionRow, sectionCol)
            cellWidth, cellHeight = getCellSize(app)
            cellWidth*=3
            cellHeight*=3
            drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                    fill=None, border= app.sectionBoxesColor,
                    borderWidth=app.cellBorderWidth)
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def boardScreen_drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    
    cellWidth, cellHeight = getCellSize(app)
    color = getCellColor(app, row, col)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border= app.lineColor,
             borderWidth=app.cellBorderWidth)
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def getCellColor(app, row, col):
    selectedRow, selectedCol = app.selectedCell
    color = None
    
    if (row, col) == app.selectedCell:
        color = rgb(183, 202, 241)
    elif row == selectedRow or col == selectedCol:
        color = rgb (217, 231, 241)
    #color the box
    elif isInBox(app, row,col):
        color = rgb (217, 231, 241)#same as prev
    return color

def getSelectBoxRegion(app, row,col):
    #find startRow and startCol
    boxSize =3
    startRow = row//boxSize *3
    startCol = col//boxSize *3
    return startRow, startCol
    


def isInBox(app, row,col):
    #given arb row and col, determine if should be highlighted
    selectedRow, selectedCol = app.selectedCell
    startRow, startCol = getSelectBoxRegion(app, selectedRow, selectedCol)
    #if inside the box of this
    return startRow<=row<startRow+3 and startCol<=col<startCol+3
        

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def getCellSize(app):
    cellWidth = app.boardWidth / app.state.cols
    cellHeight = app.boardHeight / app.state.rows
    return (cellWidth, cellHeight)
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

#cell selection
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.state.rows) and (0 <= col < app.state.cols):
        return (row, col)
    else:
        return None

#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187


