import copy
from readingInputs import*

class State:
    def __init__(self, board):
        self.rows = 9
        self.cols = 9
        self.orginalBoard = copy.deepcopy(board) #stores og board
        self.userBoard = board
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
    '''
    state.set(self, row, col, value)
  * state.ban(self, row, col, values)
  * state.unban(self, row, col, values)
    '''
def testingState():
    testBlock = State(getBoardIn2dList('easy-01.png.txt'))
    print(testBlock.getCellRegions(4,5))

testingState()