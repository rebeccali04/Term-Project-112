from cmu_graphics import *

from runAppWithScreens import *
from screen1 import *
# from mainScreen import *
# from boardScreen import *
# from inputBoardScreen import *
# from modeScreen import *
# from helpScreen import *
# from preferencesScreen import *

def onAppStart(app):
    print('In onAppStart')

def onAppStop(app):
    print('In onAppStop')

##################################
# main
##################################


def main():
    runAppWithScreens(initialScreen='screen1', width=800, height =600)

main()