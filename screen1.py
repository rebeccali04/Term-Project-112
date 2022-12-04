from cmu_graphics import *

##################################
# Screen1
##################################

def screen1_onAppStart(app):
    print('In screen1_onAppStart')
    app.color = 'gold'
    app.activatedCounter1 = 0

def screen1_onScreenActivate(app):
    print('In screen1_onScreenActivate')
    app.activatedCounter1 += 1

def screen1_onKeyPress(app, key):
    if key == 's': setActiveScreen('screen2')
    elif key == 'c': app.color = 'navy' if (app.color == 'gold') else 'gold'

def screen1_redrawAll(app):
    drawLabel('Screen 1', app.width/2, 30, size=16)
    drawLabel('Press c to change square color', app.width/2, 50, size=16)
    drawLabel('Press s to change screen to screen2', app.width/2, 70, size=16)
    drawRect(100, 100, app.width-200, app.height-200, fill=app.color)
    drawLabel(f'Screen1 was activated {app.activatedCounter1} times',
              app.width/2,app.height-30, size=12)