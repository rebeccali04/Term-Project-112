import copy
from readingInputs import *

class State:
    def __init__(self, board):
        self.rows = 9
        self.cols = 9
        self.originalBoard = copy.deepcopy(board) #stores og board
        self.userBoard = self.getEmptyBoard()
        self.legals = self.getInitalLegals()
        self.setInitalBoard(board)
        self.userLegals =self.getInitalLegals()
        

    def setInitalBoard(self,board):
        for row in range(self.rows):
            for col in range(self.cols):
                val =board[row][col]
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

    def unban(self, row, col, values):
        legalSet = self.legals[row][col]
        self.legals[row][col] = legalSet.union(values)
    
    def undoSet(self, row, col, currLegals):
        cellVal = self.userBoard[row][col]
        self.userBoard[row][col] =0
        self.unban(row, col, currLegals)
        for region in self.getCellRegions(row, col):
            for location in region:
                if self.canAdd(*location, cellVal):
                    self.unban(*location, {cellVal})

    def canAdd(self,row,col, num):
        allCellRegions = self.getCellRegions(row,col)
        for region in allCellRegions:
            if num in region:
                return False
        return True
    
    def inputLegals(self, row, col, val):
        legalSet = self.userLegals[row][col]
        if val in legalSet:
            legalSet.remove(val)
        else:
            legalSet.add(val)
    #need to test

    ########HINTS##############
    def playHint1(self):
        for row in range(self.rows):
            for col in range(self.cols):
                legalSet =self.legals[row][col]
                if len(legalSet) ==1:
                    self.set(row, col, legalSet.pop())
                    return 


#########################################
#          Test and debug               #
#########################################
    #fix, can't find print2dList
    # def printBoard(self): print2dList(self.board)
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

def testingState():
    testBlock = State(getBoardIn2dList('easy-01.png.txt'))
    # testBlock.legals = [[{1, 2, 3, 4, 5, 6, 7, 8, 9}, {1, 2, 3, 4, 5, 6, 7, 8, 9}],[]]
    # testBlock.set(0,1,8)
    # testBlock.ban(0,0,{1,2,3})
    # print(testBlock.legals)
    # testBlock.unban(0,0,{1,2,6})
    print('testing state class----------------------------\n')
    prevLegals = testBlock.legals
    currLegals = testBlock.legals[0][1]
    testBlock.set(0,1,8)
    testBlock.printLegals()
    testBlock.undoSet(0,1, currLegals)
    print('-------------------')
    testBlock.printLegals()
    assert(testBlock.legals ==prevLegals)
    print('passed')
# testingState()