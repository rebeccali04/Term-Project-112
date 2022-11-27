try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from mainScreen import *
from boardScreen import *

##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen='boardScreen', width=800, height =600) 

main()