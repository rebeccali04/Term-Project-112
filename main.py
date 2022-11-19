try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from screen1 import *
from boardScreen import *

##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen='boardScreen', width=600, height =600)

main()