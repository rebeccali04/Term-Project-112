try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from Buttons import *
from readingInputs import *


def preferencesScreen_onScreenStart(app):
    app.settingDict = eval(readFile("userPreferences.txt"))
    app.preferencesScreenButtons = [] #(msg, top, left, length, height, hover)
    setAllButtons(app)
    app.linearChoiceY = [300,400,500]
    app.currentRGB = [0,0,0]

def preferencesScreen_redrawAll(app):
    rectBottom = len(app.msgs)*20
    drawTitle(app, "Preferences Setting",)
    drawAllButtons(app.preferencesScreenButtons)  
    drawLinearChoice(app)
    drawSampleColor(app)

def preferencesScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app.preferencesScreenButtons, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.preferencesScreenButtons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app.preferencesScreenButtons)

def preferencesScreen_onMouseDrag(app, mouseX, mouseY):
    senseLinearChoice(app, mouseX, mouseY)

def preferencesScreen_onMousePress(app, mouseX, mouseY):
    senseLinearChoice(app, mouseX, mouseY)
    buttonClickedIndex = getButtonClicked(app.preferencesScreenButtons, mouseX, mouseY)
    prevMode = app.currMode
    if buttonClickedIndex ==0:
        #back
        print('back')
        setActiveScreen('mainScreen')

    elif buttonClickedIndex ==1:
        #Save changes
        # writePreferences()
        pass

def preferencesScreen_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('mainScreen')

def senseLinearChoice(app, mouseX, mouseY):
    #for on mouse press and hold
    startX = getLineStartX()
    currentLineIndex = None
    #find which line selected
    for index in range(len(app.linearChoiceY)):
        Y = app.linearChoiceY[index]
        if Y-5 <=mouseY <= Y+5:
            currentLineIndex = index
    
    print(currentLineIndex)
    
    if currentLineIndex != None:
        if startX <= mouseX <=startX+255:
            #change RGB val
            app.currentRGB[currentLineIndex] = mouseX -startX
            print(f'mouseX = {mouseX}')
            print(f'app.currentRGB[currentLineIndex] = {app.currentRGB[currentLineIndex]}')


def getLineStartX():
    return 300

def drawSampleColor(app):
    color = rgb(*app.currentRGB)
    drawRect(650,300,50,50, fill = color)

def drawLinearChoice(app):
    startX = getLineStartX()
    endX = startX+255
    msg ='RGB'
    for index in range(3):
        Y = app.linearChoiceY[index]
        drawLine(startX, Y, endX, Y, lineWidth = 2,)
        choiceX = app.currentRGB[index] +startX
        drawCircle(choiceX, Y, 5, border = 'black', fill = rgb(196, 156, 145)) #button color

        #label
        drawLabel(f'{msg[index]} = {app.currentRGB[index]}', startX, Y-50, size =14, bold =True)
    
 


def setAllButtons(app):
    # centerX = app.width/2 - 150/2
    # startY = 225
    setButton(app.preferencesScreenButtons, 'Back',50 , 40, length =60, height =40)
    setButton(app.preferencesScreenButtons, 'Save Changes', 125 , 40, length =125, height =40)
    

def drawTitle(app, msg, size =40):
    centerX = app.width/2
    drawLabel(msg, centerX, 150, size = size, bold = True, fill = rgb(196, 156, 145))

def testFunction():
    strDict = str({'background': None, 'emptyCell': None, "initialVals":'black'})
    newDict = eval(strDict)
    settingDict = eval(readFile("userPreferences.txt"))
    print(settingDict['emptyCell'])

testFunction()
