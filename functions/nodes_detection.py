import os, datetime, sys
sys.path.append('..')

import cv2
import numpy as np

from functions.params import ROOT,PLAN_ROOT,VISUALS,PLAN_PNG

def nodes_detection(auto_complete,grid,floor):
    #usual procedure while using computer vision. Set to gray, then Threshold it. (Black and white)
    gray = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    #Get read of Lines respectively Horizontal and Vertical
    mod = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 8)))
    mod2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 2)))
    #The overlapping pixels are the nodes.
    erase = cv2.bitwise_and(mod, mod2)
    #Save the nodes and display it () For possible visual checking.
    erase = (erase * 255).astype(np.uint8) if erase.dtype != np.uint8 else erase
    if not auto_complete == 'yes':
        cv2.imshow('', mod)
        cv2.imshow('.', mod2)
        cv2.imshow(',', erase)

    else:
        cv2.imwrite(os.path.join(os.getcwd(),VISUALS,f'{floor}', f'{floor}_NODES_DETECTION.png'), erase)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print('nodes_detection -Status: Done')
    
    return erase