import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import cv2

def rotate_png(auto_complete,plan,grid):
    """
      90 degrees rotation of a png file
      return png files
    """
    frame = np.rot90(plan)
    grid_frame = np.rot90(grid)
    if not auto_complete=='yes':
        cv2.imshow('Image', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('rotate_png -Status: Done')
    return frame,grid_frame