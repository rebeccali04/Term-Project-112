try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
# from DesignAssets import *
##################################
# mainScreen
##################################

def mainScreen_onScreenStart(app):
    app.buttons = [] #(msg, top, left, length, height, hover)
    setAllButtons(app)
def mainScreen_onKeyPress(app, key):
    if key == 'space': setActiveScreen('boardScreen')


def mainScreen_redrawAll(app):
    
    drawTitle(app, "SUDOKU",)
    drawAllButtons(app)

def drawTitle(app, msg, size =40):
    centerX = app.width/2
    drawLabel(msg, centerX, 150, size = size, bold = True, fill = rgb(196, 156, 145))

def mainScreen_onMouseMove(app, mouseX, mouseY):
    buttonClickedIndex = getButtonClicked(app, mouseX, mouseY)
    if buttonClickedIndex != None:
        app.buttons[buttonClickedIndex]['hover'] =True
    else:
        setAllButtonHoverFalse(app)  

def getButtonClicked(app, mouseX, mouseY):
    for index in range(len(app.buttons)):
        button = app.buttons[index]
        top = button['top']
        left = button['left']
        length = button['length']
        height = button['height']
        if left <= mouseX <= left+length and top <= mouseY <= top+height:
            return index  
    return None

def setAllButtonHoverFalse(app):
    for button in app.buttons:
        button['hover']= False

def setAllButtons(app):
    centerX = app.width/2 - 150/2
    startY = 225
    setButton(app, 'Play',centerX , startY,)
    setButton(app, 'Mode', centerX, startY+80*1,)
    setButton(app, 'Input Board', centerX, startY+80*2,)
    setButton(app, 'How to Play', centerX, startY+80*3,)
def setButton(app, msg, left, top, hover = False, length=150, height=50):
    buttonDict = {'msg': msg, 'top': top, 'left': left, 'length': length, 'height':height, 'hover': hover}
    app.buttons.append(buttonDict)

def drawAllButtons(app):
    for button in app.buttons:
        drawButton1(button['msg'], button['left'], button['top'], hover = button['hover'],length = button['length'],height = button['height'])

def drawButton1(msg, left, top, hover = False, length=150, height=50, color = rgb(169, 191, 241), fontSize =14, ):
    centerX = left+length/2
    centerY = top+height/2
    if not hover:
        drawRect(left,top, length, height, fill = None, border= color, )
        drawLabel(msg, centerX, centerY, fill = color,size =fontSize,bold =True)
    else:
        drawRect(left,top, length, height, fill = color, border= color)
        drawLabel(msg, centerX, centerY, fill = 'white',size =fontSize, bold =True)