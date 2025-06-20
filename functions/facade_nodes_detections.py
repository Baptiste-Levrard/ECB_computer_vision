import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS
from functions.rotate_points_with_cv2 import rotate_points_with_cv2

import cv2
import numpy as np

def facade_nodes_detections(grid_cropped,floor,new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2,black_background,auto_complete,angle_facade_auto):
    '''
    
    cXorient=int. Centroid of the image used to calculate the rotation of the pixels
    cYorient=int. Centroid of the image used to calculate the rotation of the pixels
    '''
    #Morient_calculations = cv2.getRotationMatrix2D((cXorient, cYorient), angle_calculation, 1.0)
    ss = np.expand_dims((new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2),axis=1)
    gray = cv2.cvtColor(grid_cropped, cv2.COLOR_BGR2GRAY)
    _, thrshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    # Create a mask with the same dimensions as the image, initialized to zeros (black)
    mask = np.zeros(thrshold.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [ss], 255)
    roi = cv2.bitwise_and(thrshold, thrshold, mask=mask)
    if auto_complete == 'yes':
        angle_facade_rotation=angle_facade_auto
    else:
        while True:
            try:
                angle_facade_rotation = float(input(f"Input angle_facade_rotation. Align vertically and horizontaly the facade plan's grid. (float): ").strip().lower())
                break
            except ValueError:
                print("Invalid input. ")
        
    # Create a mask with the same dimensions as the image, initialized to zeros (black)
    (h, w) = roi.shape[:2]
    (cXorient, cYorient) = (w // 2, h // 2)
    Morient = cv2.getRotationMatrix2D((cXorient, cYorient), angle_facade_rotation, 1.0)
    M_back = cv2.getRotationMatrix2D((cXorient, cYorient), -angle_facade_rotation, 1.0)
    rotated = cv2.warpAffine(roi, Morient, (w, h))
    mod = cv2.morphologyEx(rotated, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 12)))
    mod2 = cv2.morphologyEx(rotated, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (12, 2)))
    #The overlapping pixels are the nodes.
    erase = cv2.bitwise_and(mod, mod2)
    
    #Save the nodes and display it () For possible visual checking.
    erase = (erase * 255).astype(np.uint8) if erase.dtype != np.uint8 else erase
    mask = (erase >= 75) & (erase <= 255)
    # Set all non-white pixels to 0
    erase_cleaned = np.zeros_like(erase)
    erase_cleaned[mask] = 255
    
    
    #rotated = cv2.warpAffine(eros, M_back, (w, h))
    if not auto_complete == 'yes':
        cv2.imshow('Facade plan', roi)
        cv2.imshow('Facade plan rotated with the given angle',rotated)
        cv2.imshow('Vertical lines detection', mod)
        cv2.imshow('Horizontal lines detection', mod2)
        cv2.imshow('Intersections of both lines', erase)
        cv2.imshow('Intersections of both types of lines', erase_cleaned)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('facade_nodes_detections -Status: ongoing')
    
    contour, hier = cv2.findContours(erase_cleaned,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    centroids = []
    for cnt in contour:
        try:
            mom = cv2.moments(cnt)
            (x,y) = int(mom['m10']/mom['m00']), int(mom['m01']/mom['m00'])
            centroids.append((x,y))
        except:
            pass
            
    facade_points = np.vstack((centroids))
    facade_points_rotated_back = rotate_points_with_cv2(centroids, M_back)
    #rotation_calculation = rotate_points_with_cv2(facade_points_rotated_back, Morient_calculations)


    for i in facade_points_rotated_back:
        cv2.circle(black_background, (i[0],i[1]), radius=0, color=(0, 255, 255), thickness=3)

    if not auto_complete == 'yes':
        cv2.imshow('Visualisation of the nodes position on floors plan', black_background)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('facade_nodes_detections -Status: Done')
    return facade_points,facade_points_rotated_back,angle_facade_rotation,cXorient, cYorient,h,w