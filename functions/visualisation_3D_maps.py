import os, datetime, sys
sys.path.append('..')

import cv2
import numpy as np
import random

#Call a local function that was manually and gpt made
from functions.rotate_points_with_cv2 import rotate_points_with_cv2
from functions.params import ROOT,VISUALS

def visualisation_3D_maps(room_pixels,floor, area_threshold, vertex_threshold,number_false_room,bbox_area,aspect_ratio_threshold,angle_calculation,area_threshold_bigger_rooms,balcony_area_detected):
    if not os.path.exists(os.path.join(VISUALS,f'{floor}','3D_images')):
        os.mkdir(os.path.join(VISUALS,f'{floor}','3D_images'))
    for x_room in room_pixels:
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
    
        black_background = np.zeros_like(gray)
        
        # Loop through the contours, excluding the first one (which is usually the whole image border)
        for i, c in enumerate(sorted_contours[number_false_room:]):
            area = cv2.contourArea(c)
            M = cv2.moments(c)
            if area > area_threshold:
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    centroides_y_values.append(cy)
                    centroides_x_values.append(cx)
                    
        sorted_centroides_y = sorted(centroides_y_values)
        for i, c in enumerate(sorted_contours[number_false_room:]):
            area = cv2.contourArea(c)
            M = cv2.moments(c)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            if area > area_threshold:
                # Approximate the contour to a polygon
                epsilon = 0.01 * cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, epsilon, True)
                num_vertices = len(approx)
        
                #If there a floor is  south side and composed of a passerelle, then the two bottom rooms are not to be taken in the contours detections (as they are the passerelle and balcony)
                if 'HS' in image_name:
                    if cy not in sorted_centroides_y[:2]:
                        x, y, width, height = cv2.boundingRect(c)
                        aspect_ratio = width / float(height)
                        bbox = width * height
                        if area >= bbox_area * bbox:
                            if aspect_ratio > aspect_ratio_threshold:
                                if i == x_room:
                                    cv2.drawContours(black_background, [c], -1, (205,250,255), thickness=cv2.FILLED)
                                else:
                                    cv2.drawContours(black_background, [c], -1, (75,75,75), thickness=cv2.FILLED)
        
                        elif num_vertices < vertex_threshold or area > area_threshold_bigger_rooms:
                            if i == x_room:
                                cv2.drawContours(black_background, [c], -1, (205,250,255), thickness=cv2.FILLED)
                            else:
                                cv2.drawContours(black_background, [c], -1, (75,75,75), thickness=cv2.FILLED)
                #If there a floor is  north side and composed of a passerelle, then the two bottom rooms are not to be taken in the contours detections (as it is the balcony and passerelle)           
                if 'HN' in image_name:
                    if cy not in sorted_centroides_y[-2:]:
                        x, y, width, height = cv2.boundingRect(c)
                        aspect_ratio = width / float(height)
                        bbox = width * height
                        if area >= bbox_area * bbox:
                            if aspect_ratio > aspect_ratio_threshold:
                                if i == x_room:
                                    cv2.drawContours(black_background, [c], -1, (205,250,255), thickness=cv2.FILLED)
                                else:
                                    cv2.drawContours(black_background, [c], -1, (75,75,75), thickness=cv2.FILLED)    
                            
                        elif num_vertices < vertex_threshold or area > area_threshold_bigger_rooms:
                            if i == x_room:
                                cv2.drawContours(black_background, [c], -1, (205,250,255), thickness=cv2.FILLED)
                            else:
                                cv2.drawContours(black_background, [c], -1, (75,75,75), thickness=cv2.FILLED)
        #As of 17/02/2025 this commented section is supposed to crop the room and save it.
        #It should be used later on in the processing of the creation of the 3DDashboard. For an illustration of the floor and room we are on
        #Get the bounding box of the contour
        # Crop the region
        # Save the cropped image
        #cv2.imwrite(os.path.join('PLAN','CROPPED', f'test_room_{i}.png'), cropped_image)
        #Rotate the final picture back
        
        # Display the results
        cv2.imwrite(os.path.join(VISUALS,f'{floor}','3D_images',f'{floor}_{x_room}_IMAGE_3D.png'),black_background)
    print('visualisation_3D_maps -Status: Done')
        
    #Floor string
    return floor