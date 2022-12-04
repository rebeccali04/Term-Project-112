from cmu_graphics import *

# from runAppWithScreens import *
from State import *
import math
from readingInputs import *
from Buttons import *
from boardSolver import boardSolverMain
##################################
# boardScreen
##################################

#Todo
# inputing numbers function

def boardScreen_onAppStart(app):
    app.boardLeft = app.width*0.1
    app.boardTop = app.height*0.15
    boardSideLen = min(app.width*0.8,app.height*0.8)
    app.boardWidth = boardSideLen
    app.boardHeight = boardSideLen
    app.cellBorderWidth = 2
    app.lineColor = 'gray'
    app.boarderColor ='black'
    app.sectionBoxesColor = 'black'
    app.competitionMode = False
    restartBoardScreen(app)

def restartBoardScreen(app):
    app.boardContent =loadRandomBoard(app.currMode)
    app.currInputMode = 'normal' #other option include mouse, key
    app.boardScreenButtons = []
    #load board
    newBoard(app)
    app.selectedCell = (0,0)
    app.inputingLegals =False
    app.gameOver = False
    app.state.gameStarted = True
    app.prevStepLegals = None 

def newBoard(app):
    app.state = State(app.boardContent)
    #move to mode
    if app.currMode == 'easy':
        app.usingAutoLegals = False
    else: 
        app.usingAutoLegals =True
    app.solvedBoard = boardSolverMain(app.state) #will not modify
    setAllButtons(app)

#optional if switch board
def loadNewBoard(app, boardContent):
    app.boardContent = boardContent
    newBoard(app)

def boardScreen_onKeyPress(app, key):
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

def doInputNum(app, num):
    row,col = app.selectedCell
    row,col = app.selectedCell
    app.prevStepLegals = app.state.getLegals(row, col)
    if not app.state.cellInOriginalBoard(row,col):
        if app.inputingLegals: 
            if not app.usingAutoLegals:
                app.state.inputLegals(row, col, num)
        else:
            app.state.set(row, col,num )
    

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


def boardScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.boardScreenButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.boardScreenButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.boardScreenButtons)

def boardScreen_redrawAll(app):
    drawBackground(app)
    boardScreen_drawBoard(app)
    boardScreen_drawBoardBorder(app)
    boardScreen_DrawSectionBoxes(app)
    drawSudokuNumbers(app, app.state.userBoard)
    drawAllLegals(app)
    drawAllButtons(app.boardScreenButtons)
    drawMsg(app)
    # drawAllRedDot(app)
    #mouse only
    if app.currInputMode == 'mouse':
        drawNumPad(app)
    ########################################################
    #                      Buttons                         #
    ########################################################

def setAllButtons(app):
    y = 40
    setButton(app.boardScreenButtons, 'Back',50 , y, length =60, height =40)
    setButton(app.boardScreenButtons, 'Singleton',125 , y,length =100, height =40)
    setButton(app.boardScreenButtons, 'New Game',250 , y,length =100, height =40)
    setButton(app.boardScreenButtons, 'Auto/Manual Legals',375 , y,length =150, height =40) #make togging button
    
    ########################################################
    #                      Hints                         #
    ########################################################
def highlightHint(app):
    hint1Res = app.state.getHint1()
    if hint1Res != None:
        row, col = hint1Res
    else:
        hint2Res = app.state.getHint2()
        if hint2Res != None:
            row, col = hint2Res
        else:
            return
    #sets app.selection to this cell
    app.selectedCell = row, col
        

    ########################################################
    #                      HELPERS                         #
    ########################################################
def drawAllRedDot(app):
    #error checking kinda slow?
    errorList = findErrors(app, app.solvedBoard, app.state.userBoard)
    #competitionMode
    if app.competitionMode and errorList !=[]:
        assert(False) #crash if red
    for row, col in errorList:
        drawRedDot(app, row, col)

def findErrors(app, solvedBoard, userBoard):
    errorList = []
    for row in range(app.state.rows):
        for col in range(app.state.cols):
            if userBoard[row][col] != 0: #only check nonempty cell
                if userBoard[row][col] != solvedBoard[row][col]:
                    errorList.append((row, col))
    return errorList

def drawRedDot(app,row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawCircle(cellLeft+0.8*cellWidth, cellTop +0.8*cellHeight, 0.1*cellWidth, fill = 'red')

def drawMsg(app):
    if app.state.gameOver:
        drawRect(app.boardLeft+app.boardWidth/2, app.boardTop + app.boardHeight/2, 500, 50, align = 'center', fill  = app.settingDict['Game Over Color']) #gameOverColor
        drawLabel('Congrats, you finished the game', app.boardLeft+app.boardWidth/2, app.boardTop + app.boardHeight/2, size = 20, bold = True, fill = 'white') 
        writeFile(f'finished.txt', getStandardFormat(app.state.userBoard))

def getStandardFormat(board):
    res = ''
    for rowList in board:
        for colCell in rowList:
            res+=f'{colCell} '
        res = res[:-1]
        res+='\n'
    return res

def drawNumPad(app):
    startTop, w, h = getNumPadInfo(app)
    #draw the legal button
    
    for num in range(0,10): #numbers 1 to 9
        drawNumPadCell(app,num, startTop, w, h)
        drawNumPadNumbers(app,num, startTop, w,h )

def getNumPadInfo(app):
    #startTop, w, h
    return (app.boardTop, 50,50)

def drawNumPadCell(app,num, startTop, w,h ):
    rectX = app.width -w
    rectY = startTop +(num-1)*h
    color =None
    if num ==0 and app.inputingLegals:
        color = rgb(183, 202, 241)
    drawRect(rectX, rectY, w, h, fill =color, border ='black')

def drawNumPadNumbers(app,num, startTop, w,h ):
    numX = app.width -w/2
    numY = startTop +(num-1)*h +h/2
    msg = str(num)
    if num ==0:
        msg = 'Legal'
    drawLabel(msg, numX, numY, size = app.height//40, bold = True)

def getNumPadCell(app, mouseX, mouseY):
    startTop, w, h = getNumPadInfo(app)
    for num in range(0,10):
        rectX = app.width - w
        rectY = startTop + (num-1)*h
        if rectX <= mouseX <= rectX+w and rectY <= mouseY <= rectY+h:
            return num
    return None

def drawSudokuNumbers(app, boardToDraw):
    cellWidth, cellHeight = getCellSize(app)
    for row in range(app.state.rows):
        for col in range(app.state.cols):
            color = rgb(175, 125, 119) if not app.state.cellInOriginalBoard(row,col) else app.settingDict['Inital Values Color']
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellX = cellLeft+cellWidth/2
            cellY = cellTop +cellHeight/2
            num =boardToDraw[row][col]
            if num!=0:
                drawLabel(str(num),cellX, cellY, size = app.height//25, bold = True, fill =color)
                
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
def drawBackground(app):
    drawRect(0,0, app.width, app.height, fill = app.settingDict['Background Color'])

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
    color = app.settingDict['Empty Cell Color']
    
    if (row, col) == app.selectedCell:
        color = app.settingDict['Selected Cell Color'] #selectedCellC
    elif  isInBox(app, row,col) or row == selectedRow or col == selectedCol:
        color = app.settingDict['Selected Region Color'] 
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

