import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import cv2
import pandas as pd
import csv

from functions.rotate_points_with_cv2 import rotate_points_with_cv2
from functions.params import ROOT,VISUALS

def get_value_coordinate_horizontal(df,x_to_a_index):
    '''
    Quick and dirty fix
    Helper function to retrieve corresponding Coordinate number to corresponding coordinates pixels. Horizontal version.
    '''
    return x_to_a_index.get((df['x_axis_angle_floor'], df['y_axis_angle_floor']))

def get_value_coordinate_vertical(df,y_to_l_index):
    '''
    Quick and dirty fix
    Helper function to retrieve corresponding Coordinate number to corresponding coordinates pixels. Vertical version.
    '''
    return y_to_l_index.get((df['x_axis_angle_floor'], df['y_axis_angle_floor']))

def north_building_floor_pixels_coordinates(floor,letter_horizontal,letter_vertical,floor_points,floor_points_rotated_back,angle_floor_rotation,cXorient, cYorient,h, w,auto_complete,tolerance_x_floor_auto,tolerance_y_floor_auto,y_threshold_floor_auto,a_index_floor_auto):
    '''
    Extract the pixels coordinates of the plans nodes. Rotate the pixels so they aligned verticaly and horizontaly. Sort the pixels in a vertical and horizontal (Left to right, Top to bottom), assign the correct Plan coordinates to them. add everything in a Df.
    
    cXorient=int. Centroid of the image used to calculate the rotation of the pixels
    cYorient=int. Centroid of the image used to calculate the rotation of the pixels
    angle_calculation=int. Inherited from previous script. Help to have an angle of calculation that is the same around the whole script.
    floor_points=list. List of int, representing all the pixels coordinates of Nodes coordinates of non rotated images.
    floor=str. The floor used for the script. Must be spelled HN05 or HS04...
    a_index=int. ECB's plans and coordinates never start at the same coordinate. Need to be able to coordinate this for each floor.

    return
    floor_points_df = dataframe
    rotated = image cv2 format
    '''
#####
#####
    if auto_complete == 'yes':
        tolerance_x=tolerance_x_floor_auto
    else:
        while True:
            try:
                tolerance_x=int(input(f"Previous versions of the function worked by approximating the position of a pixel. This a reminiscent of those version but find utility when two pixels are found very close to each other to name it the same number. tolerance_x Basis 8 (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
##### 
#####
#####
    if auto_complete == 'yes':
        tolerance_y=tolerance_y_floor_auto
    else:
        while True:
            try:
                tolerance_y=int(input(f"Previous versions of the function worked by approximating the position of a pixel. This a reminiscent of those version but find utility when two pixels are found very close to each other to name it the same number. tolerance_y Basis 17 (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
##### 
#####
#####
    if auto_complete == 'yes':
        y_threshold=y_threshold_floor_auto
    else:
        while True:
            try:
                y_threshold=int(input('The possible threshold between two points being the same coordinate . y_threshold Basis 30 (int): ').strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####     
#####
#####
    if auto_complete == 'yes':
        a_index=a_index_floor_auto
    else:
        while True:
            try:
                a_index=int(input(f" ECB's plans and coordinates never start at the same coordinate. Need to be able to coordinate this for each floor. Where does {letter_horizontal} start ? (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####      
    
    #Image that do not have any calculation value, but representation value - Enable to represent easily the place of the coordinates.
    image = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_Grid.png'))
    a_save=a_index
    Morient = cv2.getRotationMatrix2D((cXorient, cYorient), angle_floor_rotation, 1.0)
    angle_floor_rotation_centroides = rotate_points_with_cv2(floor_points_rotated_back, Morient)
    #Creation of the DF variable that will hold the full coordinates (rotated and non rotated) as well as the names of those coordinates.
    floor_points_df = pd.DataFrame()

    #Create two four columns in the df to hold the corresponding non rotated and rotated pixels cooredinates
    for idx,i in enumerate(zip(floor_points_rotated_back,floor_points,angle_floor_rotation_centroides)):
        temp = pd.DataFrame(
            {
                'x_axis': i[0][0],
                'y_axis': i[0][1],
                'x_axis_rotated': i[1][0],
                'y_axis_rotated': i[1][1],
                'x_axis_angle_floor' : i[2][0],
                'y_axis_angle_floor' : i[2][1]
            },index=[idx]
        )
    
        floor_points_df = pd.concat([floor_points_df, temp])

    #Sort the rotated pixels cooredinates to get the correct name of the Axis coordinates
    floor_points_df = floor_points_df.sort_values('x_axis_rotated')
    
    #Rotate the image for a better visualisation

    rotated = cv2.warpAffine(image, Morient, (w, h))

    #Working with the variable roation rathe than the columns becasue the original code was scripted this way, hence winning time on developping a solution
    rotation = sorted(angle_floor_rotation_centroides, key=lambda c: c[0])

    # Initialize variables for grouping
    tolerance_x = tolerance_x  # Tolerance for A
    tolerance_y = tolerance_y   # Tolerance for L
    y_threshold = y_threshold  # Threshold for comparing first y-coordinates
    
    a_index = a_index #What number should it start from
    x_to_a_index = {}
    current_group = []
    
    # Group points by x-coordinate with tolerance
    for x, y in rotation:
        if not current_group or abs(x - current_group[-1][0]) <= tolerance_x:
            current_group.append((x, y))
        else:
            # Assign the current group an A index
            a_index += 1
            for gx, gy in current_group:
                x_to_a_index[gx, gy] = a_index
            # Start a new group
            current_group = [(x, y)]
    
    # Assign the last group if it exists
    if current_group:
        a_index += 1
        for gx, gy in current_group:
            x_to_a_index[gx, gy] = a_index
    
    # Map for storing Q indices
    y_to_l_index = {}
    previous_first_ys = []
    
    # Iterate over each vertical cluster and assign Q index
    for a_index in set(x_to_a_index.values()):
        # Filter points for the current A group
        group_points = [(x, y) for (x, y), a in x_to_a_index.items() if a == a_index]
        # Sort these points by y-coordinate in descending order
        group_points.sort(key=lambda point: point[1], reverse=True)
    
        # Determine Q index starting point
        if len(previous_first_ys) >= 2 and any(
            (group_points[0][1] - prev_y) > y_threshold for prev_y in previous_first_ys[-2:]
        ):
            l_index_start = 2
        else:
            l_index_start = 1
    
        # Update the history of previous first y-coordinates
        previous_first_ys.append(group_points[0][1])
        current_y_group = []
        l_index = l_index_start - 1
    
        # Group by y-coordinate and assign Q index
        for x, y in group_points:
            if not current_y_group or abs(y - current_y_group[-1][1]) <= tolerance_y:
                current_y_group.append((x, y))
            else:
                # Assign the current group a Q index
                l_index += 1
                for gx, gy in current_y_group:
                    y_to_l_index[gx, gy] = l_index
                # Start a new y group
                current_y_group = [(x, y)]
    
        # Assign the last y group if it exists
        if current_y_group:
            l_index += 1
            for gx, gy in current_y_group:
                y_to_l_index[gx, gy] = l_index
    
    # Assign labels and draw the coordinates and centers
    for x, y in rotation:
        a_idx = x_to_a_index[int(x), int(y)]
        l_idx = y_to_l_index[x, y]
        label = f"{letter_horizontal}{a_idx:02d}{letter_vertical}{l_idx:02d}"
        position = (int(x), int(y))
        cv2.putText(rotated, label, position, cv2.FONT_HERSHEY_PLAIN, 0.5, (100, 100, 100), 1)
        #cv2.circle(rotated, (x, y), radius=0, color=(0, 0, 255), thickness=3) For more precision precisely where the node land.
    
    # Display the image
    if not auto_complete == 'yes':
        cv2.imshow('Image with Custom Labels', rotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('north_building_floor_pixels_coordinates -Status: Done')
    #Add the Textual Numerical Nodes coordinates to the final DF
    floor_points_df['letter_horizontal'] = letter_horizontal
    floor_points_df['coordinate_horizontal'] = floor_points_df.apply(lambda row: get_value_coordinate_horizontal(row, x_to_a_index), axis=1)
    floor_points_df['letter_vertical'] = letter_vertical
    floor_points_df['coordinate_vertical'] = floor_points_df.apply(lambda row: get_value_coordinate_vertical(row, y_to_l_index), axis=1)

    return floor_points_df,tolerance_x,tolerance_y,y_threshold,a_save