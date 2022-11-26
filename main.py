try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from mainScreen import *
from boardScreen import *

##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen='mainScreen', width=800, height =800) 

main()