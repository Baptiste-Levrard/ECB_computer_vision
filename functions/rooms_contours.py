#Most important part of the script yet, Find the contours of the rooms, rank them by areas, draw their contours.
#Retrive the rooms pixels area
#Call Room_pixel to get the arrays ; Check if it call the whole image and the whole structure respectively in 0 and 1
#The hyperparameters are hard coded and at the minute no proper way to to get them

import os, datetime, sys
sys.path.append('..')

import cv2
import numpy as np
import random
import pickle

#Call a local function that was manually and gpt made
from functions.rotate_points_with_cv2 import rotate_points_with_cv2

from functions.params import ROOT,PLAN_ROOT,VISUALS,PLAN_PNG

def rooms_contours(plan_cropped,floor,auto_complete,area_threshold_auto,vertex_threshold_auto,number_false_room_auto,area_threshold_bigger_rooms_auto,bbox_area_auto,aspect_ratio_threshold_auto,balcony_area_detected_auto):
#####
#####    
    if auto_complete == 'yes':
        area_threshold=area_threshold_auto
    else:
        while True:
            try:
                area_threshold=float(input(f"Input area_threshold. Shapes that are under will not be considered as rooms. Basis 308.5 (float): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
##### 
#####
#####
    if auto_complete == 'yes':
        vertex_threshold=vertex_threshold_auto
    else:
        while True:
            try:
                vertex_threshold=int(input(f"Input vertex_threshold. Shapes that have more edges are not considered as rooms. Basis 4 (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####     
#####
#####
    if auto_complete == 'yes':
        number_false_room=number_false_room_auto
    else:
        while True:
            try:
                number_false_room=int(input(f"Input number_false_room. False areas on image considered as rooms. Recommended to start with 0 and adjust from there (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####     
#####
#####
    if auto_complete == 'yes':
        area_threshold_bigger_rooms = area_threshold_bigger_rooms_auto
    else:
        while True:
            try:
                area_threshold_bigger_rooms = int(input(f"Input area_threshold_bigger_rooms. The number of pixels that an element should be above to always be considered as a room. Basis 10000 (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####    
#####
#####
    if auto_complete == 'yes':
        bbox_area=bbox_area_auto
    else:
        while True:
            try:
                bbox_area = float(input(f"Input bbox_area. The ratio that the room should fill the bounding box. In range(0-1) Basis 0.5 (float): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####     
#####
#####
    if auto_complete == 'yes':
        aspect_ratio_threshold=aspect_ratio_threshold_auto
    else:
        while True:
            try:
                aspect_ratio_threshold = float(input(f"Input aspect_ratio_threshold. The ratio that the width should higher than the height. In range(0-1) Basis 0.4 (float): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####         


    if auto_complete == 'yes':
        balcony_area_detected=balcony_area_detected_auto
    else:
        while True:
            try:
                balcony_area_detected = int(input(f"Input balcony_area_detected. The number of room that are at the bottom or top of the image that should not be detected. (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
    image_name = f'{floor}_90D_CROPPED.png'
    image = plan_cropped
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply a binary threshold
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    # Apply morphological operations to clean up the image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mor_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    # Find contours
    contours, hierarchy = cv2.findContours(mor_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    centroides_y_values = []
    centroides_x_values = []
    room_pixels = {}
    black_background = np.zeros_like(image)

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
                if cy not in sorted_centroides_y[:balcony_area_detected]:
                    x, y, width, height = cv2.boundingRect(c)
                    aspect_ratio = width / float(height)
                    bbox = width * height
                    if area >= bbox_area * bbox:
                        if aspect_ratio > aspect_ratio_threshold:
                            cv2.drawContours(black_background, [c], -1, (random.randrange(50, 255), random.randrange(50, 255), random.randrange(50, 255)), thickness=cv2.FILLED)
                            mask = np.zeros_like(image)
                            cv2.fillPoly(mask, np.int32([c]), color=(0, 255, 0))
                            mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                            coordinates = np.column_stack(np.where(mask_gray > 0))
                            room_pixels[i] = coordinates

                    elif num_vertices < vertex_threshold or area > area_threshold_bigger_rooms:
                        cv2.drawContours(black_background, [c], -1, (random.randrange(50, 255), random.randrange(50, 255), random.randrange(50, 255)), thickness=cv2.FILLED)
                        mask = np.zeros_like(image)
                        cv2.fillPoly(mask, np.int32([c]), color=(0, 255, 0))
                        mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                        coordinates = np.column_stack(np.where(mask_gray > 0))
                        room_pixels[i] = coordinates

            #If there a floor is  north side and composed of a passerelle, then the two bottom rooms are not to be taken in the contours detections (as it is the balcony and passerelle)           
            if 'HN' in image_name:
                if cy not in sorted_centroides_y[-balcony_area_detected:]:
                    x, y, width, height = cv2.boundingRect(c)
                    aspect_ratio = width / float(height)
                    bbox = width * height
                    if area >= bbox_area * bbox:
                        if aspect_ratio > aspect_ratio_threshold:
                            cv2.drawContours(black_background, [c], -1, (random.randrange(50, 255), random.randrange(50, 255), random.randrange(50, 255)), thickness=cv2.FILLED)
                            mask = np.zeros_like(image)
                            cv2.fillPoly(mask, np.int32([c]), color=(0, 255, 0))
                            mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                            coordinates = np.column_stack(np.where(mask_gray > 0))
                            room_pixels[i] = coordinates
                        
                    elif num_vertices < vertex_threshold or area > area_threshold_bigger_rooms:
                        cv2.drawContours(black_background, [c], -1, (random.randrange(50, 255), random.randrange(50, 255), random.randrange(50, 255)), thickness=cv2.FILLED)
                        mask = np.zeros_like(image)
                        cv2.fillPoly(mask, np.int32([c]), color=(0, 255, 0))
                        mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                        coordinates = np.column_stack(np.where(mask_gray > 0))
                        room_pixels[i] = coordinates            

    #As of 17/02/2025 this commented section is supposed to crop the room and save it.
    #It should be used later on in the processing of the creation of the 3DDashboard. For an illustration of the floor and room we are on
    #Get the bounding box of the contour
    # Crop the region
    # Save the cropped image
    #cv2.imwrite(os.path.join('PLAN','CROPPED', f'test_room_{i}.png'), cropped_image)
    #Rotate the final picture back
    with open(os.path.join(VISUALS,f'{floor}',f'{floor}_room_pixels.pkl'), 'wb') as f:
        pickle.dump(room_pixels, f)
#    black_background_reoriented = cv2.warpAffine(black_background, M_back, (w, h))
    # Display the results
    if not auto_complete == 'yes':
        cv2.imshow('black_background_reoriented Image', black_background)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('rooms_contours -Status: Done')
    cv2.imwrite(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_Blacked.png'), black_background)
# Usage example
    return black_background,centroides_y_values,centroides_x_values,sorted_contours,room_pixels,sorted_centroides_y,area_threshold,vertex_threshold,number_false_room,area_threshold_bigger_rooms,bbox_area,aspect_ratio_threshold,balcony_area_detected