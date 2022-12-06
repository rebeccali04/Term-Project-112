try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from boardScreen import *
from runAppWithScreens import *
from Buttons import *

def twoPlayerScreen_onScreenStart(app):
    
    app.twoPlayerButtons = []
    setTwoPlayerButtons(app)
    
    app.stepsPerSecond = 1
    restartGame(app)
    
def restartGame(app):
    app.gamePaused = True #should be True in the begining
    app.twoPlayerButtons[2]['msg'] = 'Start'
    app.twoPlayerMsg = "It's Player 1's turn"
    app.playerTurn = 1 # 1 or 2
    app.player1Score = 0
    app.player1VisibleScore = app.player1Score
    app.player2Score = 0
    app.player2VisibleScore = app.player2Score
    app.timeLeft = 30 #change to 30
    app.viewingInstruction =False
    app.currBoardStatus = [0,0,0]
    updateBoardStatus(app)#cells, regions, red dot
    
    
def twoPlayerScreen_onStep(app):
    if not app.gamePaused:
        takeStep(app)
    if app.state.gameOver and not app.gamePaused:
        updateScoresAfterTurn(app)
        changePause(app)

def takeStep(app):
    updateIndividualScore(app)
    if app.timeLeft >0:
        app.timeLeft-=1
    elif app.timeLeft ==0:
        switchTurns(app)
    


def switchTurns(app):
    updateScoresAfterTurn(app)
    updateBoardStatus(app) #keep track of prev round's cell, row, col

    #change turns
    if app.playerTurn ==1:
        app.playerTurn =2
    else:
        app.playerTurn =1
    app.timeLeft = 30
    app.twoPlayerMsg = f"It's Player {app.playerTurn}'s turn"
    # app.state.resetRedoList() #not needed?
    # app.state.resetUndoList()
     
    
    changePause(app)

def twoPlayerScreen_redrawAll(app):
    drawBackground(app)
    boardScreen_drawBoard(app)
    boardScreen_drawBoardBorder(app)
    boardScreen_DrawSectionBoxes(app)
    drawSudokuNumbers(app, app.state.userBoard)
    drawAllLegals(app)
    drawAllRedDot(app)
    drawTwoPlayerStats(app)
    drawAllButtons(app.twoPlayerButtons)

    #2 player specific
    if app.gamePaused:
        drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
                    fill= app.settingDict['Selected Region Color'], )
        if app.viewingInstruction:
            drawTwoPlayerInstructions(app)
        else:
            drawLabel(f'Player {app.playerTurn}, press start to begin', 
                        app.boardLeft +app.boardWidth/2, app.boardTop +app.boardHeight/2, size =16, bold = True)
            drawLabel('Press i for instructions', 
                        app.boardLeft +app.boardWidth/2, app.boardTop +app.boardHeight/2 +30, size =14)
        
    if app.state.gameOver:
        drawGameOver(app)        
    

def drawTwoPlayerInstructions(app):
    instruction = '''
    Here's the rules:
    Each player gets 30 seconds to make moves
    Each correct cell you fill gets you 1 point
    Each row, column or box you fill gets 
    you 2 extra points
    Don't erase previous correct cells 
    (that will cost you points)
    Erase any errors ASAP
    Small hint press 'o' cost 1.5 points
    Big hint press 'p' cost 2.5 points
    Press i to view/hide this instruction while paused 
    Have fun!
    '''
    msgs = []
    for line in instruction.splitlines():
        if line !='\n':
            msgs.append(line)
    for index in range(len(msgs)):
        msg = msgs[index]
        y = index*25 +100
        drawLabel(msg, 100, y, size =16, fill = 'black', align = 'left')
    

def twoPlayerScreen_onKeyPress(app, key):
    if key == 'o':
        addPointToCurrPlayer(app, -1.5)
    elif key == 'p':
        addPointToCurrPlayer(app, -2.5)
    elif key == 'i':
        if app.gamePaused:
            app.viewingInstruction = not app.viewingInstruction
    boardScreenKeyPress(app, key) 

def twoPlayerScreen_onKeyRelease(app,key):
    boardScreenKeyRelease(app,key)

def twoPlayerScreen_onMousePress(app,mouseX,mouseY):
    boardScreenDoMousePress(app,mouseX, mouseY)
    #for two player specific
    buttonClickedIndex = getButtonClicked(app.twoPlayerButtons, mouseX, mouseY)
    if buttonClickedIndex == 0:
        #back
        setActiveScreen('mainScreen')
    elif buttonClickedIndex == 1:
        #new game
        restartBoardScreen(app)
        restartGame(app)
    elif buttonClickedIndex == 2:
        if not app.state.gameOver:
            changePause(app)

def changePause(app):
    app.gamePaused = not app.gamePaused
    if app.gamePaused:
        app.twoPlayerButtons[2]['msg'] = 'Start'
    else:
        app.twoPlayerButtons[2]['msg'] = 'Pause'

def twoPlayerScreen_onMouseMove(app, mouseX, mouseY):
    boardScreenMouseMove(app,mouseX,mouseY)
    buttonClickedIndex = getButtonClicked(app.twoPlayerButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.twoPlayerButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.twoPlayerButtons)

def addPointToCurrPlayer(app, points):
    if app.playerTurn ==1:
        app.player1Score+=points
    else:
        app.player2Score+=points

def updateIndividualScore(app):
    baseLineCells, baseLineRegions, baseLineErrors = app.currBoardStatus
    #get score change from baseline score status
    currCells= getCompletedCells(app)
    currRegions = getCompletedRegions(app)
    currErrors = getNumberOfErrors(app)
    deltaScore = (currCells-baseLineCells) + 2*(currRegions -baseLineRegions) - 0.5*(currErrors - baseLineErrors)
    #actually deduct score for errors
    print(f'currCells {currCells}')
    print(f'currRegions {currRegions}')
    print(f'currErrors {currErrors}')
    if app.playerTurn ==1:
        app.player1VisibleScore=app.player1Score +deltaScore
        app.player1Score -= 0.5*(currErrors-baseLineErrors)
    else:
        app.player2VisibleScore=app.player2Score +deltaScore
        app.player2Score -= 0.5*(currErrors-baseLineErrors)

def updateBoardStatus(app):
    #change baseline score status, modifies app.currBoardStatus
    currCells= getCompletedCells(app)
    currRegions = getCompletedRegions(app)
    currErrors = getNumberOfErrors(app)
    app.currBoardStatus = [currCells, currRegions, currErrors]


def getCompletedCells(app):
    count =0
    for row in range(app.state.rows):
        for col in range(app.state.cols):
            if app.state.userBoard[row][col] == app.state.solvedBoard[row][col]:
                count+=1
    return count

def getCompletedRegions(app):
    count =0
    for region in app.state.getAllRegions():
        if isRegionComplete(app,region):
            count+=1
    return count

def isRegionComplete(app,region):
    for row, col in region:
        if app.state.userBoard[row][col] != app.state.solvedBoard[row][col]:
            return False
    return True

def getNumberOfErrors(app):
    return len(app.state.errorList)

def updateScoresAfterTurn(app):
    app.player1Score = app.player1VisibleScore 
    app.player2Score = app.player2VisibleScore 

def drawGameOver(app):
    if app.state.gameOver:
        drawRect(app.boardLeft+app.boardWidth/2, app.boardTop + app.boardHeight/2, 500, 50, align = 'center', fill  = app.settingDict['Game Over Color']) #gameOverColor
        winner = getWinner(app)
        if winner != 'tie':
            msg = f'Game Over, Player {winner} won'
        else:
            msg = f'Game Over, it was a tie'
        drawLabel(msg, app.boardLeft+app.boardWidth/2, app.boardTop + app.boardHeight/2, size = 20, bold = True, fill = 'white') 

def getWinner(app):
    if app.player1Score > app.player2Score:
        return 1
    elif app.player1Score < app.player2Score:
        return 2
    else:
        return 'tie'

def drawTwoPlayerStats(app):
    drawRect(600, 200, 140,200, fill = app.settingDict['Selected Region Color'], border = 'black')
    drawLabel(f'Player 1 score: {app.player1VisibleScore}', 610,220, align = 'left', size =14)
    drawLabel(f'Player 2 score: {app.player2VisibleScore}', 610,250, align = 'left', size =14)
    drawLabel(app.twoPlayerMsg, 610, 280, align = 'left', size =14)
    
    #timer
    drawRect(620, 320, 100,50, fill = 'white')
    color = 'black' if app.timeLeft >5 else 'red'
    drawLabel(f'Time left: {app.timeLeft}', 630, 345, align = 'left', bold =True, size =14, fill = color)

def setTwoPlayerButtons(app):
    y = 40
    setButton(app.twoPlayerButtons, 'Back',50 , y, length =60, height =40)
    setButton(app.twoPlayerButtons, 'New Game',125 , y,length =100, height =40)
    setButton(app.twoPlayerButtons, 'Start', 250, y, length =60, height =40)