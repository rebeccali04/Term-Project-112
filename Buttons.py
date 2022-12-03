try: from cmu_cs3_graphics import *
except: from cmu_graphics import *
def getButtonClicked(buttonsList, mouseX, mouseY):
    for index in range(len(buttonsList)):
        button = buttonsList[index]
        top = button['top']
        left = button['left']
        length = button['length']
        height = button['height']
        if left <= mouseX <= left+length and top <= mouseY <= top+height:
            return index  
    return None

def setAllButtonHoverFalse(buttonsList):
    for button in buttonsList:
        button['hover']= False

def drawAllButtons(buttonsList):
    for button in buttonsList:
        drawButton1(button['msg'], button['left'], button['top'], hover = button['hover'],length = button['length'],height = button['height'])

#button color
def drawButton1(msg, left, top, hover = False, length=150, height=50, color = rgb(169, 191, 241), fontSize =14, ):
    centerX = left+length/2
    centerY = top+height/2
    if not hover:
        drawRect(left,top, length, height, fill = None, border= color, )
        drawLabel(msg, centerX, centerY, fill = color,size =fontSize,bold =True)
    else:
        drawRect(left,top, length, height, fill = color, border= color)
        drawLabel(msg, centerX, centerY, fill = 'white',size =fontSize, bold =True)
    
def setButton(buttonList, msg, left, top, hover = False, length=150, height=50):
    buttonDict = {'msg': msg, 'top': top, 'left': left, 'length': length, 'height':height, 'hover': hover}
    buttonList.append(buttonDict)

