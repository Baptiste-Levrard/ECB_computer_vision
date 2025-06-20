import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS
from functions.rotate_points_with_cv2 import rotate_points_with_cv2

import cv2
import numpy as np

def floor_nodes_detections(grid_transfer,floor,new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2,black_background,auto_complete,angle_floor_auto,kernel_size_auto):
    black_background2 = black_background.copy()
    #Morient_calculations = cv2.getRotationMatrix2D((cXorient, cYorient), angle_calculation, 1.0)
    ss = np.expand_dims((new_resized_point1,new_resized_point2,new_resized_point4,new_resized_point3),axis=1)
    gray = cv2.cvtColor(grid_transfer, cv2.COLOR_BGR2GRAY)
    mask = np.ones(gray.shape[:2], dtype=np.uint8)*255
    cv2.fillPoly(mask, [ss], 0)
    roi = cv2.bitwise_and(gray, gray, mask=mask)
    roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
    if auto_complete == 'yes':
        angle_floor_rotation=angle_floor_auto
    else:
        while True:
            try:
                angle_floor_rotation = float(input(f"Input angle_floor_rotation. Align vertically and horizontaly the floor plan's grid. (float): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
    if auto_complete == 'yes':
        kenrel_size=kernel_size_auto
    else:
        while True:
            try:
                kenrel_size = int(input(f"Input kernel_size. The edge of the mask leave some white borders. Shrinking is enable to have a proper contour, kernerl_size is one of the main component. Basis 6 (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
    # Create a mask with the same dimensions as the image, initialized to zeros (black)
    (h, w) = roi.shape[:2]
    (cXorient, cYorient) = (w // 2, h // 2)
    Morient = cv2.getRotationMatrix2D((cXorient, cYorient), angle_floor_rotation, 1.0)
    M_back = cv2.getRotationMatrix2D((cXorient, cYorient), -angle_floor_rotation, 1.0)
    
    rotated = cv2.warpAffine(roi, Morient, (w, h))
    
    black_background_for_nodes_detection = np.zeros_like(rotated)
    contours, hierarchy = cv2.findContours(cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY),cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    cv2.fillPoly(black_background_for_nodes_detection, contours, color=(255, 255, 255))
    kernel = np.ones((kenrel_size, kenrel_size), np.uint8)  # Adjust the kernel size for different offsets
    black_background_for_nodes_detection = cv2.erode(black_background_for_nodes_detection, kernel, iterations=1)
    black_background_for_nodes_detection = cv2.cvtColor(black_background_for_nodes_detection, cv2.COLOR_BGR2GRAY)
    
    _, rotated = cv2.threshold(rotated, 240, 255, cv2.THRESH_BINARY_INV)
    mod = cv2.morphologyEx(rotated, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 12)))
    mod2 = cv2.morphologyEx(rotated, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (12, 2)))
    #The overlapping pixels are the nodes.
    erase = cv2.bitwise_and(mod, mod2,mask=black_background_for_nodes_detection)
    #Save the nodes and display it () For possible visual checking.
    erase = (erase * 255).astype(np.uint8) if erase.dtype != np.uint8 else erase
    
    if not auto_complete == 'yes':
        cv2.imshow('floor plan', roi)
        cv2.imshow('mod',mod)
        cv2.imshow('mod2',mod2)
        cv2.imshow('erase',erase)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('floor_nodes_detections -Status: ongoing')
    erase = cv2.cvtColor(erase, cv2.COLOR_BGR2GRAY)
    contour, hier = cv2.findContours(erase,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    centroids = []
    for cnt in contour:
        try:
            mom = cv2.moments(cnt)
            (x,y) = int(mom['m10']/mom['m00']), int(mom['m01']/mom['m00'])
            centroids.append((x,y))
        except:
            pass
            
    floor_points = np.vstack((centroids))
    floor_points_rotated_back = rotate_points_with_cv2(centroids, M_back)
    #rotation_calculation = rotate_points_with_cv2(floor_points_rotated_back, Morient_calculations)
    
    for i in floor_points_rotated_back:
        cv2.circle(black_background2, (i[0],i[1]), radius=0, color=(0, 0, 255), thickness=3)
        cv2.circle(black_background, (i[0],i[1]), radius=0, color=(0, 0, 255), thickness=3)
    
    if not auto_complete == 'yes':
        cv2.imshow('Visualisation of the nodes position on floors plan', black_background2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('floor_nodes_detections -Status: Done')
    return floor_points,floor_points_rotated_back,angle_floor_rotation,kenrel_size,cXorient, cYorient,h, w