#Functions to Tranfer the room's floor shape onto the grid image & the nodes image
#Taking most of the rooms_contours.py fuctions; Selecting the necessary elements of an image by their centers depending of the floor
import os, datetime, sys
sys.path.append('..')

import cv2
import numpy as np
import random

from functions.params import ROOT,PLAN_ROOT,VISUALS,PLAN_PNG

def transfer_grid(floor,angle_calculation,auto_complete,number_false_room_transfer_auto,number_balcony_transfer_room_auto):
#####
#####
    if auto_complete == 'yes':
        number_false_room=number_false_room_transfer_auto
    else:
        while True:
            try:
                number_false_room=int(input(f"Input number_false_room_grid. False areas on image considered as rooms. Recommended to start with 0 and adjust from there (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####
#####
#####
    if auto_complete == 'yes':
        number_balcony_transfer_room=number_balcony_transfer_room_auto
    else:
        while True:
            try:
                number_balcony_transfer_room=int(input(f"Input number_balcony_transfer_room. Areas at the balcony place. Helps delimitating the shape of the transfer of the grid. Recommended to start with previous balcony number and adjust from there (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
##### 
    
    image_name = f'{floor}_90D_CROPPED.png'
    #Will have to be modified when the 
    image = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_90D_CROPPED.png'))
    # rotate our image by 45 degrees around the center of the image
    #Using unrotated plans from the ecb, everything is inclined of 7 degrees. Making it straight help us to detect accuratly top and bottom rooms.
    #Why ?
    #Because we are focusing on their center, and inclined rooms might have a center lower or higher than some rooms
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Apply a binary threshold
    _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    # Apply morphological operations to clean up the image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    mor_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    # Find contours
    contours, hierarchy = cv2.findContours(mor_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    centroides_y_values = []
    centroides_x_values = []

    test =  np.zeros_like(gray)
    black_background = np.zeros_like(gray)

    #18/02/2025 Now that I'm thinking about it why not changing the detection of the room center by the room bottom/top pixels?
    for i, c in enumerate(sorted_contours[number_false_room:]):
        area = cv2.contourArea(c)
        M = cv2.moments(c)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            centroides_y_values.append(cy)
            centroides_x_values.append(cx)
    all_points = []
    sorted_centroides_y = sorted(centroides_y_values)
    for i, c in enumerate(sorted_contours[number_false_room:]):
        area = cv2.contourArea(c)
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.drawContours(test, [c], -1, (75,75,75), thickness=cv2.FILLED)

        #If there a floor is  south side and composed of a passerelle, then the two bottom rooms are not to be taken in the contours detections (as they are the passerelle and balcony)
        if 'HS' in image_name:
            if cy not in sorted_centroides_y[:number_balcony_transfer_room]:
                epsilon = 0.001 * cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, epsilon, True)
                all_points.append(approx.squeeze())
        #If there a floor is  north side and composed of a passerelle, then the two bottom rooms are not to be taken in the contours detections (as it is the balcony and passerelle)           
        elif 'HN' in image_name:
            if cy not in sorted_centroides_y[-number_balcony_transfer_room:]:
                all_points.append(c.squeeze())

    combined_points = np.vstack(all_points)
    hull = cv2.convexHull(combined_points)
    cv2.fillPoly(black_background, [hull], color=(255, 255, 255))
    cv2.polylines(black_background,[hull],True,(255,255,255),12)

    #M_back = cv2.getRotationMatrix2D((cXorient, cYorient), -angle_calculation, 1.0)
    #black_background = cv2.warpAffine(black_background, M_back, (w, h))
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    #black_background = cv2.dilate(black_background,kernel,iterations=5)
    
    
    other_image = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_90D_CROPPED_GRID.png'))
    other_image = cv2.resize(other_image, (image.shape[1], image.shape[0]))#The size could be an issue if the procedure is not followed accuratly.
    other_image2 = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_NODES_DETECTION.png'))
    other_image2 = cv2.resize(other_image2, (image.shape[1], image.shape[0]))#The size could be an issue if the procedure is not followed accuratly.

    
    masked_image = cv2.bitwise_and(other_image, other_image, mask=black_background)
    masked_image2= cv2.bitwise_and(other_image2, other_image2, mask=black_background)
    # Show the masked image
    if not auto_complete == 'yes':
        cv2.imshow('blacked_image', black_background)#helps to visualize the concept
        cv2.imshow(f'{floor}_grid', masked_image)
        cv2.imshow(f'{floor}_nodes', masked_image2)
        cv2.imshow('other_image', other_image)#Visualize which image has been selected
        cv2.imshow('contours', test)#
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('transfer_grid -Status: Done')
    cv2.imwrite(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_Grid.png'), masked_image)
    cv2.imwrite(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_Nodes.png'), masked_image2)
    
    return black_background,masked_image,masked_image2,number_false_room,number_balcony_transfer_room