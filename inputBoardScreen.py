try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from boardScreen import loadNewBoard
from Buttons import *
from State import *
import math
import copy

def inputBoardScreen_onScreenStart(app):
    restartInputBoardScreen(app)

def restartInputBoardScreen(app):
    app.inputState = State(getEmptyBoard())
    app.inputBoardScreenButtons=[]
    app.inputSelectedCell = (0,0)
    setAllButtons(app)
    #text file input
    app.clickedInputBox = False
    app.inputStr = ''

def inputBoardScreen_redrawAll(app):
    boardScreen_drawBoard(app)
    boardScreen_drawBoardBorder(app)
    boardScreen_DrawSectionBoxes(app)
    drawSudokuNumbers(app, app.inputState.userBoard)
    drawAllButtons(app.inputBoardScreenButtons)
    drawFileInputItems(app)

def inputBoardScreen_onKeyPress(app, key):
    #input text file
    if app.clickedInputBox:
        app.inputStr +=key
        return
    # if key == 'space': 
    #     # app.currScreen = 'boardScreen'
    #     setActiveScreen('mainScreen')
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


def inputBoardScreen_onMousePress(app,mouseX, mouseY):
    inputSelectedCell = getCell(app, mouseX, mouseY)
    if inputSelectedCell != None:
      if inputSelectedCell != app.inputSelectedCell:
        app.inputSelectedCell = inputSelectedCell
    buttonClickedIndex = getButtonClicked(app.inputBoardScreenButtons, mouseX, mouseY)
    if buttonClickedIndex ==0:
        #back
        setActiveScreen('mainScreen')
    elif buttonClickedIndex ==1:
        #clear
        restartInputBoardScreen(app)
        app.inputStr = ''
    elif buttonClickedIndex ==2:
        #done
        if app.inputStr != '':
            try: 
                boardPath = loadBoardPaths([app.inputStr])
                assert(len(boardPath)==1)
                loadNewBoard(app,getBoardIn2dList(boardPath[0]))
            except:
                app.inputStr = "Can't find this file"
        else:
            loadNewBoard(app.inputState.userBoard)
            
    elif buttonClickedIndex ==3:
        #play
        print('play button')
        setActiveScreen('boardScreen')

    #input cell
    if clickInInputCell(app, mouseX, mouseY):
        app.clickedInputBox =True
    else: 
        app.clickedInputBox =False

def inputBoardScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.inputBoardScreenButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.inputBoardScreenButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.inputBoardScreenButtons)




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
                drawLabel(str(num),cellX, cellY, size = app.height//25, bold = True, fill =color)

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
#modified, originally from https://cs3-112-f22.academy.cs.cmu.edu/notes/4187

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


########################
#      Buttons         #
########################
def setAllButtons(app):
    y = 40
    setButton(app.inputBoardScreenButtons, 'Back',50 , y, length =60, height =40)
    setButton(app.inputBoardScreenButtons, 'Clear',125 , y,length =100, height =40)
    setButton(app.inputBoardScreenButtons, 'Done',250 , y,length =100, height =40)
    setButton(app.inputBoardScreenButtons, 'Play',375 , y,length =100, height =40)



########################
#      FileImport         #
########################

def drawFileInputItems(app):
    drawLabel('To enter a board by text file,', app.width -230, 125, size =14, align ='left')
    drawLabel('place the file in the boards folder', app.width -230, 150, size =14, align ='left')
    drawLabel('then type your file name (after board\)', app.width -230, 175, size =14, align ='left')
    drawRect(app.width -230, 200, 200, 30, fill = rgb(217, 231, 241))
    drawLabel(app.inputStr, app.width -230, 215, size =15, align ='left', fill = rgb(175, 125, 119))


def clickInInputCell(app,mouseX, mouseY):
    #200 30
    if app.width-230 <= mouseX <= app.width-230 +200 and 200 <= mouseY <= 200+30:
        return True
    else:
        return False



    