import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import cv2

def resize_image(frame,grid_frame,original_points,auto_complete,x_auto,y_auto):
#####
#####    
    if auto_complete == 'yes':
        x=x_auto
    else:
        while True:
            try:
                x=int(input(f"Input x -horizontal- pixels. Basis 1900 (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input. Please enter a valid float value.")
#####
##### 
#####
#####
    if auto_complete == 'yes':
        y=y_auto
    else:
        while True:
            try:
                y=int(input(f"Input y -vertical- pixels. Basis 1004 (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input. Please enter a valid float value.")
#####
#####     
    
    original_height, original_width = grid_frame.shape[:2]
    resized_image = cv2.resize(frame, (x, y))
    resized_grid = cv2.resize(grid_frame, (x, y))
    scale_x =  x / original_width
    scale_y =  y / original_height
    resized_point1 = (int(original_points['0'][0][0] * scale_x), int(original_points['0'][0][1] * scale_y))
    resized_point2 = (int(original_points['0'][1][0] * scale_x), int(original_points['0'][1][1] * scale_y))
    resized_point3 = (int(original_points['1'][0][0] * scale_x), int(original_points['1'][0][1] * scale_y))
    resized_point4 = (int(original_points['1'][1][0] * scale_x), int(original_points['1'][1][1] * scale_y))
    
    #Plot the resized points on the resized image to have a visual validation
    resized_image_copy =resized_grid.copy()
    cv2.circle(resized_image_copy, resized_point1, 5, (0, 255, 0), -1)
    cv2.circle(resized_image_copy, resized_point2, 5, (0, 255, 0), -1)
    cv2.circle(resized_image_copy, resized_point3, 5, (0, 255, 0), -1)
    cv2.circle(resized_image_copy, resized_point4, 5, (0, 255, 0), -1)
    if not auto_complete == 'yes':
        cv2.imshow('resized_image', resized_image_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('resize_image -Status: Done')
    return resized_image, resized_grid,resized_point1,resized_point2,resized_point3,resized_point4,x,y