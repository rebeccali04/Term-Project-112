try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from mainScreen import *
from boardScreen import *
from inputBoardScreen import *
from modeScreen import *
from helpScreen import *
from preferencesScreen import *
from twoPlayerScreen import *
##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen='twoPlayerScreen', width=800, height =600)

main()