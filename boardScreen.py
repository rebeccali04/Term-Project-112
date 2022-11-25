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

def boardScreen_onScreenStart(app, board = None):
    app.boardLeft = app.width*0.1
    app.boardTop = app.height*0.15
    app.boardWidth = app.width*0.8
    app.boardHeight = app.height*0.8
    app.cellBorderWidth = 2
    app.lineColor = 'gray'
    app.boarderColor ='black'
    app.sectionBoxesColor = 'black'
    restartBoardScreen(app)

def restartBoardScreen(app):
    app.boardScreenButtons = []
    app.state = State(getBoardIn2dList('easy-01.png.txt'))
    app.selectedCell = (0,0)
    setAllButtons(app)

def boardScreen_onKeyPress(app, key):
    if key == 'space': setActiveScreen('mainScreen')
    if key.isdigit():
        row,col = app.selectedCell
        if not app.state.cellInOriginalBoard(row,col):
            app.state.set(row, col, int(key))


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
    elif buttonClickedIndex ==2:
        print('New Game')
    elif buttonClickedIndex ==3:
        print('legals toggle')

def boardScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.boardScreenButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.boardScreenButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.boardScreenButtons)

def boardScreen_onStep(app):
    pass
    # app.cx = (app.cx + app.dx) % app.width

def boardScreen_redrawAll(app):
    boardScreen_drawBoard(app)
    boardScreen_drawBoardBorder(app)
    boardScreen_DrawSectionBoxes(app)
    drawSudokuNumbers(app, app.state.userBoard)
    drawAllButtons(app.boardScreenButtons)

    ########################################################
    #                      Buttons                         #
    ########################################################

def setAllButtons(app):
    setButton(app.boardScreenButtons, 'Back',50 , 20, length =60, height =40)
    setButton(app.boardScreenButtons, 'Hint',150 , 20,length =60, height =40)
    setButton(app.boardScreenButtons, 'New Game',250 , 20,length =100, height =40)
    setButton(app.boardScreenButtons, 'Legals',400 , 20,length =100, height =40)


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


