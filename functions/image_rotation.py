import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import cv2

from functions.rotate_points_with_cv2 import rotate_points_with_cv2

def image_rotation(plan_resized,grid_resized,resized_point1,resized_point2,resized_point3,resized_point4,auto_complete,angle_calculation_auto):
    if auto_complete == 'yes':
        angle_calculation=angle_calculation_auto
    else:
        while True:
            try:
                angle_calculation=float(input(f"Input angle_calculation. Amgle that will put the rooms supposedly on top and on bottom according to the plan orientation. Basis 7 (float): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
    #Will have to be modified when the 
    image = plan_resized
    eros = image.copy()
    (h, w) = eros.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # rotate our image by 45 degrees around the center of the image
    #Using unplan_rotated plans from the ecb, everything is inclined of 7 degrees. Making it straight help us to detect accuratly top and bottom rooms.
    #Why ?
    #Because we are focusing on their center, and inclined rooms moght have a center lower or higher than some rooms
    M = cv2.getRotationMatrix2D((cX, cY), angle_calculation, 1.0)
    M_back = cv2.getRotationMatrix2D((cX, cY), -angle_calculation, 1.0)
    plan_rotated = cv2.warpAffine(eros, M, (w, h))
    grid_rotated = cv2.warpAffine(grid_resized, M, (w, h))
    
    points_rotated = rotate_points_with_cv2([resized_point1,resized_point2,resized_point3,resized_point4],M)
    # Perform the actual rotation and return the image

    if not auto_complete == 'yes':
        cv2.imshow('plan_rotated Image', plan_rotated)
        cv2.imshow('grid_rotated Image', grid_rotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('image_rotation -Status: Done')
    return plan_rotated,grid_rotated,points_rotated,angle_calculation