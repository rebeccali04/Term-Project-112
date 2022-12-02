import os
import random
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
#copied from piazza


def getAllFile(cwdPath):
    res = []
    for filename in os.listdir(cwdPath+'/boards'):
        if filename.endswith('.txt'):
            pathToFile = f'{cwdPath}/boards/{filename}'
            fileContents = readFile(pathToFile) #string type
            res.append(fileContents)
    return res

#copied from piazza and modified

# def getAllFile(cwdPath):
#     res = []
#     for filename in os.listdir(cwdPath+'/boards'):
#         if filename.endswith('.txt'):
#             pathToFile = f'{cwdPath}/boards/{filename}'
#             fileContents = readFile(pathToFile) #string type
#             res.append(fileContents)
#     return res
#m original

# def getThisFile(fileName):
#     cwdPath = os.getcwd()
#     pathToFile = cwdPath+ '/boards/'+fileName
#     fileContents = readFile(pathToFile)
#     return fileContents #returns a string
def getThisFile(filePath):
    fileContents = readFile(filePath)
    return fileContents #returns a string

#input example 'easy-01.png.txt'
def getBoardIn2dList(fileName):
    boardInStr = getThisFile(fileName)
    resultBoard = []
    for line in boardInStr.splitlines():
        lineList = []
        for entry in line.split(' '):
            lineList.append(int(entry))
        resultBoard.append(lineList)
    return resultBoard #return 2d Board with ints

def loadBoardPaths(filters):
    boardPaths = [ ]
    for filename in os.listdir(f'boards/'):
        if filename.endswith('.txt'):
            if hasFilters(filename, filters):
                boardPaths.append(f'boards/{filename}')
    return boardPaths

#https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html
def hasFilters(filename, filters=None):
    if filters == None: return True
    for filter in filters:
        if filter not in filename:
            return False
    return True
#https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html

def loadRandomBoardPath(filters):
    allBoadPath =loadBoardPaths(filters)
    return random.choice(allBoadPath)


def loadRandomBoard(filters=None):
    boardPath = loadRandomBoardPath(filters)
    return getBoardIn2dList(boardPath)
    
#https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html
def writeFile(path, contents):
        with open(path, "wt") as f:
            f.write(contents)
#https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html


#os.getcwd() from https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
def test():
    # print(loadRandomBoard('hard'))
    pass

test()