try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from Board import Board
import math
##################################
# Screen2
##################################

#Todo
# cell objects?


def boardScreen_onScreenStart(app):
    app.currBoard = Board.getEmptyBoard()
    app.currBoard[2][3] =7
    app.rows = 9
    app.cols = 9
    app.boardLeft = app.width*0.1
    app.boardTop = app.height*0.1
    app.boardWidth = app.width*0.8
    app.boardHeight = app.height*0.8
    app.cellBorderWidth = 2
    app.lineColor = 'gray'
    app.boarderColor ='black'
    app.sectionBoxesColor = 'black'
    app.selectedCell = (0,0)

def boardScreen_onKeyPress(app, key):
    if key == 's': setActiveScreen('screen1')

def boardScreen_onMousePress(app,mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
      if selectedCell == app.selectedCell:
          #app.selection = None
          pass
      else:
          app.selectedCell = selectedCell


def boardScreen_onStep(app):
    pass
    # app.cx = (app.cx + app.dx) % app.width

def boardScreen_redrawAll(app):
    boardScreen_drawBoard(app)
    boardScreen_drawBoardBorder(app)
    boardScreen_DrawSectionBoxes(app)
    drawSudokuNumbers(app, app.currBoard)


    ########################################################
    #                      HELPERS                         #
    ########################################################

def drawSudokuNumbers(app, boardToDraw):
    cellWidth, cellHeight = getCellSize(app)
    for row in range(app.rows):
        for col in range(app.cols):
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellX = cellLeft+cellWidth/2
            cellY = cellTop +cellHeight/2
            num =boardToDraw[row][col]
            if num!=0:
                drawLabel(str(num),cellX, cellY, size = app.width//20, bold = True)
                
                

def boardScreen_drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            boardScreen_drawCell(app, row, col)

def boardScreen_drawBoardBorder(app):
  # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border=app.boarderColor,
           borderWidth=2*app.cellBorderWidth)

def boardScreen_DrawSectionBoxes(app):
    for sectionRow in range(0,app.rows,3):
        for sectionCol in range(0,app.cols,3):
            cellLeft, cellTop = getCellLeftTop(app, sectionRow, sectionCol)
            cellWidth, cellHeight = getCellSize(app)
            cellWidth*=3
            cellHeight*=3
            drawRect(cellLeft, cellTop, cellWidth, cellHeight,
                    fill=None, border= app.sectionBoxesColor,
                    borderWidth=app.cellBorderWidth)

def boardScreen_drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    
    cellWidth, cellHeight = getCellSize(app)
    color = getCellColor(app, row, col)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border= app.lineColor,
             borderWidth=app.cellBorderWidth)

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

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

#cell selection
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)
    else:
        return None