import copy
from readingInputs import *
import itertools
# from boardSolver import boardSolverMain

class State:
    def __init__(self, board):
        self.gameOver = False
        self.gameStarted = False
        self.rows = 9
        self.cols = 9
        self.originalBoard = copy.deepcopy(board) #stores og board
        self.userBoard = self.getEmptyBoard()
        self.legals = self.getInitalLegals()
        self.setInitalBoard(board)
        self.userLegals =self.getInitalLegals()
        self.solvedBoard = None
        #front will need to set gameStarted to True
        self.undoList = []
        self.redoList = []

    def setInitalBoard(self,board):
        for row in range(self.rows):
            for col in range(self.cols):
                val = board[row][col]
                if val!= 0:
                    self.set(row,col,val)
        

    def getEmptyBoard(self): #testing purposes
        return [[0]*9 for _ in range(9)]
        
    def getInitalLegals(self):
        res = []
        for _ in range(self.rows):
            rowList =[]
            for __ in range(self.cols):
               rowList.append(self.getNineLegalVals())
            res.append(rowList)
        return res 

    def getNineLegalVals(self):
        return set([_ for _ in range(1,10)])

    def boardAllFilled(self):
            for rowList in self.userBoard:
                if 0 in rowList:
                    return False
            return True
    
    #eq
    #repr
    #hash
    
    def cellInOriginalBoard(self,row,col):
        return self.originalBoard[row][col] != 0
    
    def getRowRegion(self, row):
        #gets a list of 9 tuple of the row
        result = []
        for col in range(self.cols):
            result.append((row, col))
        return result

    def getColRegion(self, col):
        #gets a list of 9 tuple of the col
        result = []
        for row in range(self.rows):
            result.append((row, col))
        return result
        

    def getBlockRegion(self, block):
        #input is a int 0-8
        #returns a list of 9 tuples in the given block 0-8
        res = []
        startRow = block//3 *3
        startCol = block%3 *3
        
        for row in range(startRow, startRow+3):
            for col in range(startCol, startCol+3):
                res.append((row, col))
        return res

    def getBlock(self, row, col):
        #gives what block (numbered 0-8) this cell belongs to
        boxSize =3
        blockNum = row//boxSize *3 + col//boxSize
        return blockNum
        

    def getBlockRegionByCell(self, row, col):
        blockNum = self.getBlock(row, col)
        return self.getBlockRegion(blockNum)



    def getCellRegions(self, row, col):
        #returns all regions the cell belong in
        res = []
        res.append(self.getRowRegion(row))
        res.append(self.getColRegion(col))
        res.append(self.getBlockRegionByCell(row, col))
        return res

    def getAllRegions(self):
        #returns all regions on the board
        res = []
        for row in range(self.rows):
            res.append(self.getRowRegion(row))
        for col in range(self.cols):
            res.append(self.getColRegion(col))
        for blockNum in range(9):
            res.append(self.getBlockRegionByCell(row, col))
        return res

    def getAllRegionsThatContainTargets(self, targets):
        #get all row col that contains that target val in targets
        resSet = set()
        for targetVal in targets:
            for row in range(self.rows):
                for col in range(self.cols):
                    if target == self.userBoard[row][col]: 
                        resSet.add(self.getRowRegion(row))
                        resSet.add(self.getColRegion(col))
                        resSet.add(self.getBlockRegionByCell(row, col))
        return list(resSet)

    def set(self, row, col, value):
        #saves prev copy in undoList
        if self.gameStarted:
            self.undoList.append(copy.deepcopy(self))

        # place a value down on the board 
        self.userBoard[row][col] = value
        # ban all vals of this cell
        self.ban(row, col, self.getNineLegalVals())
        #all this val in all regions containing this val:
        allRegions =self.getCellRegions( row, col)
        for region in allRegions:
            for location in region:
                row, col = location
                self.ban(row,col,{value})
        self.checkForGameOver()

        #clears redoList
        if self.gameStarted:
            self.redoList = []

    def banUserLegals(self, row, col, values):
        #gets rid of the legal values in this row col cell
        legalSet = self.userLegals[row][col]
        self.legals[row][col] = legalSet.difference(values) 
        
    def unbanUserLegals(self, row, col, values):
        legalSet = self.userLegals[row][col]
        self.legals[row][col] = legalSet.union(values)
    

    def ban(self, row, col, values):
        #gets rid of the legal values in this row col cell
        legalSet = self.legals[row][col]
        self.legals[row][col] = legalSet.difference(values) 

    def unban(self, row, col, currLegals):
        legalSet = self.legals[row][col]
        self.legals[row][col] = legalSet.union(currLegals)
    
    def undoSet(self, row, col, currLegals): 
        cellVal = self.userBoard[row][col]
        self.userBoard[row][col] = 0
        self.unban(row, col, currLegals)
        for region in self.getCellRegions(row, col):
            for location in region:
                if self.canAdd(*location, cellVal):
                    self.unban(*location, {cellVal})

    def canAdd(self,row,col, num):
        #first test to see if this region if empty or not
        if self.userBoard[row][col]!= 0:
            return False
        allCellRegions = self.getCellRegions(row,col)

        for region in allCellRegions:
            for row, col in region:
                if num == self.userBoard[row][col]:
                    return False
        return True
    
    def inputLegals(self, row, col, val):
        legalSet = self.userLegals[row][col]
        if val in legalSet:
            legalSet.remove(val)
        else:
            legalSet.add(val)
    #need to test

    def checkForGameOver(self):
        if self.isGameOver():
            self.gameOver =True
        
    
    def isGameOver(self):
        if not self.boardAllFilled():
            return False
        allRegions = self.getAllRegions()
        for region in allRegions:
            if self.hasNonZeroDup(region):
                return False
        return True

    
        

    def hasNonZeroDup(self, region):
        seenVals = []
        for row, col in region:
            val = self.userBoard[row][col]
            if val!=0 and val in seenVals:
                return True
            else:
                seenVals.append(val)
        return False

    ########HINTS##############

    #returns the cell to highlight
    def getHint1(self):
        for row in range(self.rows):
            for col in range(self.cols):
                legalSet =self.legals[row][col]
                if len(legalSet) ==1:
                    return (row,col)
        # will return none if can't do anything

    #plays the move
    def playHint1(self):
        for row in range(self.rows):
            for col in range(self.cols):
                legalSet =self.legals[row][col]
                if len(legalSet) ==1:
                    self.set(row, col, legalSet.pop())
                    return 
        # will return none if can't do anything
    

    #returns the cell to highlight
    def getHint2(self): #logical error?
        for N in range(2,5):
            for region in self.getAllRegions():
                groupings = itertools.combinations(region, N)
                for group in groupings:
                    legalSet = self.containSameNLegals(group, N) #returns a legal set if yes, none if not
                    if legalSet !=None:
                        banGroup = self.getsNewBans(legalSet, group, region)
                        if banGroup != None:
                            return banGroup
        return None
    
    def playHint2(self): #logical error?
        for N in range(2,5):
            for region in self.getAllRegions():
                groupings = itertools.combinations(region, N)
                for group in groupings:
                    legalSet = self.containSameNLegals(group, N) #returns a legal set if yes, none if not
                    if legalSet !=None:
                        banGroup = self.getsNewBans(legalSet, group, region)
                        if banGroup != None:
                            self.banGroupHint2(banGroup, legalSet)
                            return 'success'
        return None
    
    def banGroupHint2(self, banGroup,legalSet):
        for row, col in banGroup:
            self.ban(row,col, legalSet)

    
    def getLegals(self, row, col):
        return self.legals[row][col]

    def containSameNLegals(self, group , N):
        legalSet =  self.getLegals(*group[0])
        #is there even N of them
        if len(legalSet) != N:
            return None

        for row, col in group:
            currLegals = self.getLegals(row,col)
            if legalSet != currLegals:
                return None
        return copy.copy(legalSet)
    
    def getsNewBans(self, legalSet, group, region):
        res = []
        for row, col in region: #for each of the cells in the region
            if (row, col) in group: #optional
                continue #looking for not in group
            currLegals = self.getLegals(row, col)
            if len(currLegals - legalSet ) ==1:
                res.append((row,col))
        if res ==[]: return None
        else: return res

    # def getHint2(self):
    #     for region in self.getAllRegions():
    #         for N in range(2, 6):
    #             result = self.applyRule2(region, N)
    #             if result != None:
    #                 return result
    #     return None

    # def applyRule2(self, region, N):
        '''
        This method uses:
            * itertools.combinations(region, N)
            * self.valuesAreOnlyLegals(values, targets)
            * self.getBansForAllRegions(values, targets)
        '''

    # def getBansForAllRegions(self, values, targets):
    #     # The values (to ban) can stay in the targets, but they must be
    #     # banned from all other cells in all regions that contain all
    #     # the targets
    #     bans = [ ]
    #     for region in self.getAllRegionsThatContainTargets(targets):




    #undo and redo
    def undo(self):
        if self.undoList == []: 
            return self
        prevState = self.undoList.pop()
        prevState.redoList += self.redoList + [self]
        return prevState
    
    def redo(self):
        if self.redoList ==[]:
            return self
        futureState = self.redoList.pop()
        futureState.undoList.append(self)
        return futureState


#########################################
#          Test and debug               #
#########################################
    #fix, can't find print2dList
    def printBoard(self): print2dList(self.userBoard)
    def printLegals(self):
        colWidth = 4
        for col in range(9):
            colWidth = max(colWidth, 1+max([len(self.legals[row][col]) for row in range(9)]))
        for row in range(9):
            for col in range(9):
                label = ''.join([str(v) for v in sorted(self.legals[row][col])])
                if label == '': label = '-'
                print(f"{' '*(colWidth - len(label))}{label}", end='')
            print()
    def print(self): self.printBoard(); self.printLegals()
#https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html

#





def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)





def print2dList(L):
    print(repr2dList(L))




def testingState():
    print('testing state class----------------------------\n')

    testBlock = State(getBoardIn2dList(loadBoardPaths(['hard-02.png.txt'])[0]))
    # testBlock.printLegals()
    # row = 0
    # col =1
    # currLegal = testBlock.legals[row][col]
    # beforeSetLegals = testBlock.legals
    # print('current legals are' )
    # print(currLegal)
    # testBlock.set(row, col, 8)
    # print('after set')
    # testBlock.printLegals()
    # print(testBlock.userBoard)
    # print('after undo set')
    # testBlock.undoSet(row, col,currLegal)
    # afterUndoSetLegals = testBlock.legals
    # testBlock.printLegals()
    # assert(beforeSetLegals ==afterUndoSetLegals)
    testBlock.printBoard()
    
    # prevLegals = testBlock.legals
    # currLegals = testBlock.legals[0][1]
    # testBlock.set(0,1,8)
    # testBlock.printLegals()
    # testBlock.undoSet(0,1, currLegals)
    # print('-------------------')
    # testBlock.printBoard()
    # assert(testBlock.legals ==prevLegals)
    
    print('passed')
# testingState()