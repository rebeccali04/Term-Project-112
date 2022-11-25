from State import *
from readingInputs import *
import time

def boardSolverMain(stateObject):
    assert(isinstance(stateObject, State))
    state =copy.deepcopy(stateObject)
    potentialRes =solveBoard(state)
    assert(potentialRes !=None)
    stateObject.solvedBoard = potentialRes

#mutating version not working
# def solveBoard(state):
#     if state.boardAllFilled():
#         return state.userBoard #done
#     else:
#         #expands cell with least legals
#         row, col = findCellWithFewestLegals(state)
#         # if state.userBoard[row][col] ==0:
#         legalsSet = state.legals[row][col]
#         for num in legalsSet:
#             if isLegal(state, row,col, num):
#                 currCellLegals = state.legals[row][col] #save for later
#                 state.set(row, col, num)
#                 potentialRes =solveBoard(state)
#                 if potentialRes !=None:
#                     return potentialRes
#                 #undo step
#                 state.undoSet(row, col, currCellLegals)
#         return None

#non mutating version
def solveBoard(state):
    if state.boardAllFilled():
        return state.userBoard #done
    else:
        
        #expands cell with least legals
        row, col = findCellWithFewestLegals(state)
        # if state.userBoard[row][col] ==0:
        for num in state.legals[row][col]:
            if isLegal(state, row,col, num):
                # print(f'trying {row},{col}')
                #create a copy 
                tempState = copy.deepcopy(state)
                tempState.set(row,col, num)
                potentialRes =solveBoard(tempState)
                if potentialRes !=None:
                    return potentialRes
        return None


def findCellWithFewestLegals(state):
    bestRow, bestCol = 0,0
    bestLegalCount = 9
    for row in range(state.rows):
        for col in range(state.cols):
            currCount = len(state.legals[row][col])
            if currCount!=0 and currCount <bestLegalCount:
                #update
                bestRow, bestCol = row, col
                bestLegalCount = currCount
    return (bestRow, bestCol)

def isLegal(state,row,col, num):
    allCellRegions = state.getCellRegions(row,col)
    for region in allCellRegions:
        if num in region:
            return False
    return True
                            
'''
def solveBoard(self):
        board = copy.deepcopy(self.orginalBoard)
        self.solvedBoard = Board.solveBoardHelper(board)

    @staticmethod
    def solveBoardHelper(board):
        #working solution
        rows, cols = len(board),len(board[0])
        if Board.boardAllFilled(board):
            return board
        else: 
            for row in range(rows):
                for col in range(cols):
                    if board[row][col] !=0: #non-empty
                        continue
                    else:
                        for num in range(1,10):
                            #put the number in
                            board[row][col] = num
                            if not Board.isLegal(board):
                                #try another
                                continue
                            
                            if Board.solveBoardHelper(board) !=None: #works
                                return board
            return None
            
        
    @staticmethod
    def boardAllFilled(board):
        for rowList in board:
            if 0 in rowList:
                return False
        return True

    @staticmethod
    def isLegal(board):
        for section in Board.getRowColSection(board):
            if Board.hasNonZeroDup(section):
                return False
        return True

    @staticmethod
    def hasNonZeroDup(section):
        seenVals = []
        for val in section:
            if val!=0 and val in seenVals:
                return True
            else:
                seenVals.append(val)
        return False
'''

#########################################
#          Test and debug               #
#########################################
def testBoardSolver(state, verbose):
    return
def testBacktracker(filters):
        time0 = time.time()
        boardPaths = sorted(loadBoardPaths(filters))
        failedPaths = [ ]
        for boardPath in boardPaths:
            board = getBoardIn2dList(boardPath)
            print(boardPath)
            solution = boardSolverMain(State(board), verbose=False)
            if not solution:
                failedPaths.append(boardPath)
        print()
        totalCount = len(boardPaths)
        failedCount = len(failedPaths)
        okCount = totalCount - failedCount
        time1 = time.time()
        if len(failedPaths) > 0:
            print('Failed boards:')
            for path in failedPaths:
                print(f'    {path}')
        percent = round(100 * okCount/totalCount)
        print(f'Success rate: {okCount}/{totalCount} = {percent}%')
        print(f'Total time: {round(time1-time0, 1)} seconds')
        
def testBoardSolver():
    pass
    # testBacktracker(filters=['hard'])
    # problems with 'easy-03' and beyond
    # boardName = 'hard-01'
    # print('testingBoardSolver')
    # testBlock = State(getBoardIn2dList(boardName+'.png.txt'))
    # # print(len(testBlock.legals[0][2]))
    # boardSolverMain(testBlock)
    # print(repr(testBlock.solvedBoard)) #infinite loop right now
    # # print(isLegal(testBlock,0,1,8)) #works
    # # testBlock.printLegals()
    # # print(findCellWithFewestLegals(testBlock))
    # assert(testBlock.solvedBoard == getBoardIn2dList(boardName +'-solution.png-solution.txt'))
    # print('passed')
    
def boardSolverTesterWithTime():
    time0 = time.time()
    boardName = 'evil-02' #taking 9 secs for evil 2
    print(f'testing solver for {boardName}')
    testBlock = State(getBoardIn2dList(boardName+'.png.txt'))
    boardSolverMain(testBlock)
    print(testBlock.solvedBoard)
    assert(testBlock.solvedBoard == getBoardIn2dList(boardName +'-solution.png-solution.txt'))
    time1 = time.time()
    print(f'Time is {time1-time0} seconds')


boardSolverTesterWithTime()
