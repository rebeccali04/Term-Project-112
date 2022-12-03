try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from Buttons import *
from readingInputs import *


def preferencesScreen_onScreenStart(app):
    app.settingDict = eval(readFile("userPreferences.txt")) #overall, used throughout the scree'Background Color'
    app.settingsCategories = list(app.settingDict)
    app.preferencesScreenButtons = [] #(msg, top, left, length, height, hover)
    setAllButtons(app)
    app.linearChoiceY = [300,400,500]
    app.currentRGB = [0,0,0]
    app.currSelectedSetting = 0

def preferencesScreen_redrawAll(app):
    rectBottom = len(app.msgs)*20
    drawTitle(app, "Preferences Setting",)
    drawAllButtons(app.preferencesScreenButtons)  
    drawLinearChoice(app)
    drawSampleColor(app)
    drawSettingSelection(app)

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
        setActiveScreen('mainScreen')

    elif buttonClickedIndex ==1:
        #Save changes
        # writePreferences()
        saveCurrentPreferences(app)
        
    elif buttonClickedIndex ==2:
        #Restore
        app.settingDict = ({'Background Color': None, 'Empty Cell Color': None, 'Inital Values Color': 'black', 'Selected Cell Color': rgb(183, 202, 241), 'Selected Region Color': rgb(217, 231, 241), 'Game Over Color': rgb(196, 156, 145), 'Titles Color': rgb(196, 156, 145)})
        saveStr = str(app.settingDict).replace(", '",",\n '")
        writeFile('userPreferences.txt',saveStr )

    changeSettingIndex(app, mouseX, mouseY)

def preferencesScreen_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('mainScreen')

def saveCurrentPreferences(app):
    updateRGBVal(app)
    saveStr = str(app.settingDict).replace(", '",",\n '")
    writeFile('userPreferences.txt',saveStr )

def senseLinearChoice(app, mouseX, mouseY):
    #for on mouse press and hold
    startX = getLineStartX()
    currentLineIndex = None
    #find which line selected
    for index in range(len(app.linearChoiceY)):
        Y = app.linearChoiceY[index]
        if Y-5 <=mouseY <= Y+5:
            currentLineIndex = index
    
    
    if currentLineIndex != None:
        if startX <= mouseX <=startX+255:
            #change RGB val
            app.currentRGB[currentLineIndex] = mouseX -startX
    
    #update RGB value
    # updateRGBVal(app)

def updateRGBVal(app):
    category = app.settingsCategories[app.currSelectedSetting]
    app.settingDict[category] = rgb(*app.currentRGB)
    #eval(f'rgb({tuple(app.currentRGB)})') #check for string to value convertion       


def getLineStartX():
    return 300

def drawSampleColor(app):
    color = rgb(*app.currentRGB)
    drawRect(650,300,50,50, fill = color, border = 'black')

def drawLinearChoice(app):
    startX = getLineStartX()
    endX = startX+255
    msg ='RGB'
    for index in range(3):
        Y = app.linearChoiceY[index]
        drawLine(startX, Y, endX, Y, lineWidth = 2,)
        choiceX = app.currentRGB[index] +startX
        drawCircle(choiceX, Y, 5, border = 'black', fill = 'black') 

        #label
        drawLabel(f'{msg[index]} = {app.currentRGB[index]}', startX, Y-50, size =14, bold =True)
    
def drawSettingSelection(app):
    startTop,left,width,height =  getSettingSelectionInfo(app)
    for index in range(len(app.settingsCategories)):
        categoryName = app.settingsCategories[index]
        color = rgb(169, 191, 241) if index == app.currSelectedSetting else None
        top = startTop + height*index
        drawRect(left, top , width, height, fill =color, border = 'black', borderWidth =1)
        drawLabel(categoryName, left +width/2, top +height/2, size = 14)
    
    #drawBorder 
    drawRect(left, startTop, width, height*len(app.settingsCategories)-1, fill =None, border = 'black', borderWidth =2 )

def changeSettingIndex(app, mouseX, mouseY):
    index = getSettingsIndex(app, mouseX, mouseY)
    if index != None and index != app.currSelectedSetting:
        app.currSelectedSetting = index
        app.currentRGB = [0,0,0]


def getSettingsIndex(app, mouseX, mouseY):
    startTop,left,width,height = getSettingSelectionInfo(app)
    for index in range(len(app.settingsCategories)):
        category = app.settingsCategories[index]
        top =  startTop + height*index
        if left <= mouseX <= left+width and top <= mouseY <= top + height:
            return index
    return None


def getSettingSelectionInfo(app):
    return 150, 50, 150, 50,  #startTop,left,width,height
    

def setAllButtons(app):
    # centerX = app.width/2 - 150/2
    # startY = 225
    setButton(app.preferencesScreenButtons, 'Back',50 , 40, length =60, height =40)
    setButton(app.preferencesScreenButtons, 'Save Changes', 400 , 550 , length =125, height =40)
    setButton(app.preferencesScreenButtons, 'Restore Default', 550, 550, length =125, height =40)

def drawTitle(app, msg, size =40):
    centerX = app.width/2
    drawLabel(msg, centerX, 100, size = size, bold = True, fill = app.settingDict['Titles Color'])
    drawLabel('Move the circle to adjust the RGB value, save each changes', centerX, 130, )

def testFunction():
    strDict = str({'background': None, 'emptyCell': None, "initialVals":'black'})
    newDict = eval(strDict)
    settingDict = eval(readFile("userPreferences.txt"))
    print(list(settingDict))

testFunction()

'''
{
'Background Color': None, 
'Empty Cell Color': None, 
'Inital Values Color':'black',
'Selected Cell Color': rgb(183, 202, 241),
'Selected Region Color': rgb(217, 231, 241),
'Game Over Color' :rgb(196, 156, 145),
'Titles Color' : rgb(196, 156, 145),
}
'''