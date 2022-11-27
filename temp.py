from State import *
import math

def mainScreen_onScreenStart(app):
    restartInputBoardScreen(app)

def restartInputBoardScreen(app):
    app.inputState = State(getEmptyBoard())
    app.mainScreenButtons=[]
    app.inputSelectedCell = (0,0)

def mainScreen_onKeyPress(app, key):
    if key == 'space': 
        # app.currScreen = 'boardScreen'
        setActiveScreen('mainScreen')
    if key.isdigit():
        row,col = app.inputSelectedCell
        val =int(key)
        app.inputState.set(row, col,val )

    if key == 'left':    moveSelection(app, 0, -1)
    elif key == 'right': moveSelection(app, 0, +1)
    elif key == 'up':    moveSelection(app ,-1, 0)
    elif key == 'down':  moveSelection(app, +1, 0) 
    #modified, from https://cs3-112-f22.academy.cs.cmu.edu/notes/4189

def moveSelection(app, drow, dcol):
    if app.inputSelectedCell != None:
        selectedRow, selectedCol = app.inputSelectedCell
        newSelectedRow = (selectedRow + drow) % app.inputState.rows
        newSelectedCol = (selectedCol + dcol) % app.inputState.cols
        app.inputSelectedCell = (newSelectedRow, newSelectedCol)
#modified, from https://cs3-112-f22.academy.cs.cmu.edu/notes/4189


def mainScreen_onMousePress(app,mouseX, mouseY):
    inputSelectedCell = getCell(app, mouseX, mouseY)
    print(inputSelectedCell)
    if inputSelectedCell != None:
      if inputSelectedCell != app.inputSelectedCell:
        app.inputSelectedCell = inputSelectedCell
    buttonClickedIndex = getButtonClicked(app.mainScreenButtons, mouseX, mouseY)
    if buttonClickedIndex ==0:
        #back
        setActiveScreen('mainScreen')
    elif buttonClickedIndex ==1:
        #clear
        restartInputBoardScreen(app)

    elif buttonClickedIndex ==2:
        #done
        print('done button')
        app.state = app.inputBoardState #test
    elif buttonClickedIndex ==3:
        #play
        print('play button')
        setActiveScreen('mainScreen')

def mainScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.mainScreenButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.mainScreenButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.mainScreenButtons)

def mainScreen_redrawAll(app):
    boardScreen_drawBoard(app)
    boardScreen_drawBoardBorder(app)
    boardScreen_DrawSectionBoxes(app)
    drawSudokuNumbers(app, app.inputState.userBoard)
    drawAllButtons(app.mainScreenButtons)



def getEmptyBoard(): 
    return [[0]*9 for _ in range(9)]

########################
#      HELPERS         #
########################

def drawSudokuNumbers(app, boardToDraw):
    cellWidth, cellHeight = getCellSize(app)
    for row in range(app.inputState.rows):
        for col in range(app.inputState.cols):
            color = 'black'
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellX = cellLeft+cellWidth/2
            cellY = cellTop +cellHeight/2
            num =boardToDraw[row][col]
            if num!=0:
                drawLabel(str(num),cellX, cellY, size = app.width//20, bold = True, fill =color)

def boardScreen_drawBoard(app):
    for row in range(app.inputState.rows):
        for col in range(app.inputState.cols):
            boardScreen_drawCell(app, row, col)
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def boardScreen_drawBoardBorder(app):
  # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border=app.boarderColor,
           borderWidth=2*app.cellBorderWidth)
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def boardScreen_DrawSectionBoxes(app):
    for sectionRow in range(0,app.inputState.rows,3):
        for sectionCol in range(0,app.inputState.cols,3):
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
    selectedRow, selectedCol = app.inputSelectedCell
    color = None
    if (row, col) == app.inputSelectedCell:
        color = rgb(183, 202, 241)
    return color


def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

def getCellSize(app):
    cellWidth = app.boardWidth / app.inputState.cols
    cellHeight = app.boardHeight / app.inputState.rows
    return (cellWidth, cellHeight)
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

#cell selection
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.inputState.rows) and (0 <= col < app.inputState.cols):
        return (row, col)
    else:
        return None

#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

#buttons
def setAllButtons(app):
    y = 40
    setButton(app.mainScreenButtons, 'Back',50 , y, length =60, height =40)
    setButton(app.mainScreenButtons, 'Clear',125 , y,length =100, height =40)
    setButton(app.mainScreenButtons, 'Done',250 , y,length =100, height =40)
    setButton(app.mainScreenButtons, 'Play',375 , y,length =100, height =40)

    