try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
from screen1 import *
from screen2 import *

##################################
# main
##################################

def main():
    runAppWithScreens(initialScreen='screen1', width=800)

main()