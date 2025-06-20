import os, datetime, sys
sys.path.append('..')

import cv2
import numpy as np

from functions.params import ROOT,PLAN_ROOT,VISUALS,PLAN_PNG

def crop_plan(auto_complete,plan,grid_plan,floor,resized_point1,resized_point2,resized_point3,resized_point4):
    img = plan
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # Apply a binary threshold
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mor_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    # Find contours
    contours, hierarchy = cv2.findContours(mor_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    min_x, min_y = np.inf, np.inf
    max_x, max_y = -np.inf, -np.inf
    
    for i, c in enumerate(sorted_contours[1:]):
        x, y, w, h = cv2.boundingRect(c)
        # Update the min and max coordinates
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)
    #If the coodinate is less than 0(Out of bound for the image), it render some weird behaviour and overall ruin the script.
    #This ensure that the minimum pixel is 0.
    min_x = max(0, min_x - 10)
    min_y = max(0, min_y - 10)
    max_x = max_x + 10
    max_y = max_y + 10

    new_resized_point1 = (resized_point1[0]-min_x),(resized_point1[1]-min_y)
    new_resized_point2 = (resized_point2[0]-min_x),(resized_point2[1]-min_y)
    new_resized_point3 = (resized_point3[0]-min_x),(resized_point3[1]-min_y)
    new_resized_point4 = (resized_point4[0]-min_x),(resized_point4[1]-min_y)
    
    cropped_image = plan[(min_y):(max_y), (min_x):(max_x)]
    cropped_grid_plan = grid_plan[(min_y):(max_y), (min_x):(max_x)]
    cropped_grid_plan_copy = cropped_grid_plan.copy()
    
    cv2.line(cropped_grid_plan_copy,new_resized_point1,new_resized_point2,(255,255,0),5)
    cv2.line(cropped_grid_plan_copy,new_resized_point3,new_resized_point4,(255,255,0),5)
    cv2.circle(cropped_grid_plan_copy,new_resized_point1 , 5, (0, 0, 0), -1)
    cv2.circle(cropped_grid_plan_copy,new_resized_point2 , 5, (0, 0, 0), -1)
    cv2.circle(cropped_grid_plan_copy,new_resized_point3 , 5, (0, 0, 0), -1)
    cv2.circle(cropped_grid_plan_copy,new_resized_point4 , 5, (0, 0, 0), -1)
    
    if not auto_complete == 'yes':
        cv2.imshow('Filtered Plan', cropped_image)
        cv2.imshow('Filtered Grid', cropped_grid_plan_copy)
    else:
        print('crop_plan -Status: Done')
    
    cv2.imwrite(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_90D_CROPPED.png'),cropped_image)
    cv2.imwrite(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_90D_CROPPED_GRID.png'),cropped_grid_plan)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return cropped_image,cropped_grid_plan,new_resized_point1,new_resized_point2,new_resized_point3,new_resized_point4