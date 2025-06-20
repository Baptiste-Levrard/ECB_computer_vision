import os, datetime, sys
sys.path.append('..')

import cv2
import numpy as np

def rotate_point(point, M_inv):
    '''
    GPT function.
    Enable a one liner for the rotation of the pixels points.
    point = int.
    M_inv = matrix
    '''
    x, y = point
    point_array = np.array([x, y, 1])
    original_point_array = M_inv @ point_array
    return int(original_point_array[0]), int(original_point_array[1])


def trapezes_lines_facade_plan(grid,auto_complete,angle1_auto,angle2_auto,min_size_trapeze_line_auto):
    """
    Detect the trapezoides lines of the facade buildings.
    angle = int. Angle will also compute the negative interger. Enbaling the clockwise rotation.
    """
    #https://pyimagesearch.com/2016/04/11/finding-extreme-points-in-contours-with-opencv/
    #Did most of the heavy lifting
#####
#####    
    if auto_complete == 'yes':
        angle1 = angle1_auto
    else:
        while True:
            try:
                angle1 = float(input(f"First input angle. How many degrees does it take to rotate the trapeze line as vertical as possible. Basis 45 (float): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
##### 
    if auto_complete == 'yes':
        angle2 = angle2_auto
    else:
        while True:
            try:
                angle2 = float(input(f"Second input angle. How many degrees does it take to rotate the trapeze line as vertical as possible. Basis 45 (float): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####   
    
    original_points = {}
    test=[]
    test_valid=[]
    angle1_variable=angle1
    angle2_variable=angle2
    angles = [angle1,angle2]
    for origine, angle in enumerate(angles):
        #Convert the grid to exploitable format
        #rotated from the decided angles
        #Better results on Thresholded image
        #Due to the way rotated images behave in CV2, have to do it on non cropped-resized images to detect trapeze lines
        #This is why it takes place very early in the script processing
        # Assuming 'grid' is your input image and 'angle' is the rotation angle
        gray = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)
        (h, w) = gray.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        
        # Calculate new dimensions to prevent cropping
        new_w = int(h * np.abs(np.sin(np.radians(angle))) + w * np.abs(np.cos(np.radians(angle))))
        new_h = int(h * np.abs(np.cos(np.radians(angle))) + w * np.abs(np.sin(np.radians(angle))))
        
        # Adjust the center for the new dimensions
        new_cX, new_cY = new_w // 2, new_h // 2
        
        # Create a larger canvas to prevent cropping
        canvas = np.zeros((new_h, new_w), dtype=gray.dtype)
        canvas[new_cY - cY:new_cY + (h - cY), new_cX - cX:new_cX + (w - cX)] = gray
        
        # Rotate the larger canvas
        M = cv2.getRotationMatrix2D((new_cX, new_cY), angle, 1.0)
        rotated = cv2.warpAffine(canvas, M, (new_w, new_h))
        
        # Threshold to create a mask
        _, mask = cv2.threshold(rotated, 240, 255, cv2.THRESH_BINARY_INV)
        
        # Morphological operations
        mod = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 12)))
        
        # Skeletonization
        img = mod
        size = np.size(img)
        skel = np.zeros(img.shape, np.uint8)
        ret, img = cv2.threshold(img, 127, 255, 0)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        done = False
        while not done:
            eroded = cv2.erode(img, element)
            temp = cv2.dilate(eroded, element)
            temp = cv2.subtract(img, temp)
            skel = cv2.bitwise_or(skel, temp)
            img = eroded.copy()
            zeros = size - cv2.countNonZero(img)
            if zeros == size:
                done = True
        
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(skel, connectivity=8)
        
        # Determine min_size
        if auto_complete == 'yes':
            min_size = min_size_trapeze_line_auto
        else:
            while True:
                try:
                    min_size = int(input("Input min_size. The minimum size of objects for them to be taken into consideration in the final skeleton form. If there is more than a line, then there is an error. Basis 40 (int): ").strip())
                    break
                except ValueError:
                    print("Invalid input.")
        
        cleaned_skeleton = np.zeros(skel.shape, dtype=np.uint8)
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] >= min_size:
                cleaned_skeleton[labels == i] = 255
        
        contours, _ = cv2.findContours(cleaned_skeleton, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c = max(contours, key=cv2.contourArea)
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        cv2.circle(cleaned_skeleton, extTop, 8, (255, 0, 0), -1)
        cv2.circle(cleaned_skeleton, extBot, 8, (255, 255, 0), -1)
        
        # Rotate back to original orientation and resize
        M_invert = cv2.getRotationMatrix2D((new_cX, new_cY), -angle, 1.0)
        rotated_back = cv2.warpAffine(rotated, M_invert, (new_w, new_h))
        
        cropped_back = rotated_back[new_cY - cY:new_cY + (h - cY), new_cX - cX:new_cX + (w - cX)]
        
        # Adjust the point coordinates accordingly
        original_point1 = rotate_point(extTop, M_invert)
        original_point2 = rotate_point(extBot, M_invert)
        cv2.circle(rotated_back, original_point1, 4, (0, 0, 0), -1)
        cv2.circle(rotated_back, original_point2, 4, (0, 0, 0), -1)
        
        # Adjust points to fit within the original cropped image
        shift_x = new_cX - cX
        shift_y = new_cY - cY
        original_point1 = (original_point1[0] - shift_x, original_point1[1] - shift_y)
        original_point2 = (original_point2[0] - shift_x, original_point2[1] - shift_y)
        
        # Plot them on the cropped_back image for validation
        cv2.circle(cropped_back, original_point1, 4, (0, 0, 0), -1)
        cv2.circle(cropped_back, original_point2, 4, (0, 0, 0), -1)

        original_points[f'{origine}'] =[original_point1,original_point2]

        if not auto_complete == 'yes':
            cv2.imshow('Rotation of the original plan, to see if it is vertical', rotated)
            cv2.imshow('', mod)
            cv2.imshow("everything shrinked ; named Skeleton",skel)
            cv2.imshow('Skeleton of the structure without superflous objects', cleaned_skeleton)
            cv2.imshow('Rotated back', rotated_back)
            cv2.imshow('cropped back', rotated_back)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print(f'trapezes_lines_facade_plan : {angle} degrees -Status: Done')
        
    return original_points,angle1_variable,angle2_variable,min_size