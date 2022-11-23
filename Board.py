import copy
from readingInputs import*
class Board:
    #pass in a 2d list of the board
    def __init__(self, board):
        self.rows = 9
        self.cols = 9
        self.orginalBoard = copy.deepcopy(board) #stores og board
        self.userBoard = board
        self.solveBoard()
        
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

    @staticmethod
    def breakToFlattenedBox(board, startRow, startCol, boxSize=3):
        #given a starting row col location, returns a 1d list of the box 
        # region of the square with side length of the boxsize
        #non mutating
        box= []
        for row in range(startRow, startRow+boxSize):
            rowList = []
            for col in range(startCol, startCol+boxSize):
                valAtIndex = board[row][col]
                rowList.append(valAtIndex)
            box.append(rowList)
        flattenedBox =[]
        for rowList in box:
            flattenedBox.extend(rowList)
        return flattenedBox

    @staticmethod
    def getRowColSection(board):
        rows, cols = len(board),len(board[0])
        #returns a list of sectiions(which are lists)
        result = []
        #get rowList
        for rowList in board:
            result.append(copy.copy(rowList))
        #get colList
        for col in range(cols):
            colList =[]
            for row in range(rows):
                colList.append(board[row][col])
            result.append(copy.copy(colList))
        #get boxes
        boxSize = int(len(board)**0.5)
        for startRow in range(0,rows,boxSize):
            for startCol in range(0, cols, boxSize):
                result.append(Board.breakToFlattenedBox(copy.deepcopy(board), 
                                startRow, startCol, boxSize))
                
        return result
    
    @staticmethod
    def getEmptyBoard(): #testing purposes
        return [[0]*9 for _ in range(9)]



#test cases
def testBoardSolver():
    print('testing board', end ='done')
    board = Board(getBoardIn2dList('easy-01.png.txt'))
    assert board.solvedBoard == getBoardIn2dList('easy-01-solution.png-solution.txt')
     
# testBoardSolver()