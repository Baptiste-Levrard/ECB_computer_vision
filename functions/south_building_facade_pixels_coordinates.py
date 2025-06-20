import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import cv2
import pandas as pd
import csv

from functions.params import ROOT,VISUALS

def south_building_facade_pixels_coordinates(floor,letter_horizontal,letter_vertical,facade_points,facade_points_rotated_back,angle_facade_rotation,cXorient, cYorient,h,w,auto_complete,tolerance_x_facade_auto,tolerance_y_facade_auto,y_threshold_facade_auto,r_index_facade_auto):
    '''
    Extract the pixels coordinates of the plans nodes. Rotate the pixels so they aligned verticaly and horizontaly. Sort the pixels in a vertical and horizontal (Left to right, Top to bottom), assign the correct Plan coordinates to them. add everything in a Df.

    cXorient=int. Centroid of the image used to calculate the rotation of the pixels
    cYorient=int. Centroid of the image used to calculate the rotation of the pixels
    facade_points=array of list. List of int, representing all the pixels coordinates of Nodes coordinates of non rotated images.
    floor=str. The floor used for the script. Must be spelled HN05 or HS04...
    letter_horizontal=str. Building's axis letter
    letter_vertical=str. Building's axis letter
    y_threshold=int.
    r_index=int. ECB's plans and coordinates never start at the same coordinate. Need to be able to coordinate this for each floor.

    return
    facade_points_df = dataframe
    rotated = image cv2 format
    '''
#####
#####    
    if auto_complete == 'yes':
        tolerance_x=tolerance_x_facade_auto
    else:
        while True:
            try:
                tolerance_x=int(input(f"Previous versions of the function worked by approximating the position of a pixel. This a reminiscent of those version but find utility when two pixels are found very close to each other to name it the same number. tolerance_x - Basis 17 (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####
    if auto_complete == 'yes':
        tolerance_y=tolerance_y_facade_auto
    else:
        while True:
            try:
                tolerance_y=int(input(f"Previous versions of the function worked by approximating the position of a pixel. This a reminiscent of those version but find utility when two pixels are found very close to each other to name it the same number. tolerance_y - Basis 5 (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####
    if auto_complete == 'yes':
        y_threshold=y_threshold_facade_auto
    else:
        while True:
            try:
                y_threshold=int(input('The possible threshold between two points being the same coordinate . y_threshold - Basis 30 (int): ').strip().lower())
                break
            except ValueError:
                print("Invalid input.")
#####
#####
    if auto_complete == 'yes':
        r_index=r_index_facade_auto
    else:
        while True:
            try:
                r_index=int(input(f"ECB's plans and coordinates never start at the same coordinate. Need to be able to coordinate this for each floor. Where does {letter_horizontal} start ? (int): ").strip().lower())
                break
            except ValueError:
                print("Invalid input.")


    
    #Has been a mismatch of the R calculation and the S calculation. The labels in the formula are switch, but the end result shows the correct labels
    image = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_Grid.png'))
    n_save=r_index
    #Creation of the DF variable that will hold the full coordinates (rotated and non rotated) as well as the names of those coordinates.
    facade_points_df = pd.DataFrame()

    #Create two four columns in the df to hold the corresponding non rotated and rotated pixels cooredinates
    for idx,i in enumerate(zip(facade_points_rotated_back,facade_points)):
        temp = pd.DataFrame(
            {
                'x_axis': i[0][0],
                'y_axis': i[0][1],
                'x_axis_rotated': i[1][0],
                'y_axis_rotated': i[1][1]
            },index=[idx]
        )
    
        facade_points_df = pd.concat([facade_points_df, temp])

    #Sort the rotated pixels cooredinates to get the correct name of the Axis coordinates
    facade_points_df = facade_points_df.sort_values('x_axis_rotated')
    
    #Rotate the image for a better visualisation
    Morient = cv2.getRotationMatrix2D((cXorient, cYorient), angle_facade_rotation, 1.0)
    rotated = cv2.warpAffine(image, Morient, (w, h))

    #Working with the variable roation rathe than the columns becasue the original code was scripted this way, hence winning time on developping a solution
    rotation = sorted(facade_points, key=lambda c: c[0])

    # Initialize variables for grouping
    tolerance_x = tolerance_x  # Tolerance for S
    tolerance_y = tolerance_y   # Tolerance for R
    y_threshold = y_threshold  # Threshold for comparing first y-coordinates
    
    r_index = r_index
    x_to_r_index = {}
    current_group = []
    
    # Group points by x-coordinate with tolerance
    for x, y in rotation:
        if not current_group or abs(x - current_group[-1][0]) <= tolerance_x:
            current_group.append((x, y))
        else:
            # Assign the current group an S index
            r_index += 1
            for gx, gy in current_group:
                x_to_r_index[gx, gy] = r_index
            # Start a new group
            current_group = [(x, y)]
    
    # Assign the last group if it exists
    if current_group:
        r_index += 1
        for gx, gy in current_group:
            x_to_r_index[gx, gy] = r_index
    
    # Map for storing R indices
    y_to_s_index = {}
    previous_first_ys = []
    last_s_index = 6
    
    # Iterate over each vertical cluster and assign R index
    for r_index in set(x_to_r_index.values()):
        group_points = [(x, y) for (x, y), a in x_to_r_index.items() if a == r_index]
    
        # Sort these points by y-coordinate
        group_points.sort(key=lambda point: point[1],reverse=True)
    
        # Determine Q index starting point
#        if len(previous_first_ys) >= 2 and any(
#            (group_points[0][1] - prev_y) > y_threshold for prev_y in previous_first_ys[-2:]
#        ):
#            s_index_start = 5
#        else:
        s_index_start = -1
    
        # Update the history of previous first y-coordinates
        previous_first_ys.append(group_points[0][1])
    
        current_y_group = []
        s_index = s_index_start + 1
    
        # Group by y-coordinate and assign R index
        for x, y in group_points:
            if not current_y_group or abs(y - current_y_group[-1][1]) <= tolerance_y:
                current_y_group.append((x, y))
            else:
                # Assign the current group a R index
                s_index += 1
                for gx, gy in current_y_group:
                    y_to_s_index[gx, gy] = s_index
                # Start a new y group
                current_y_group = [(x, y)]
    
        # Assign the last y group if it exists
        if current_y_group:
            s_index += 1
            for gx, gy in current_y_group:
                y_to_s_index[gx, gy] = s_index
    
        # Update last_r_index for the next group
        last_r_index = r_index
    
    # Assign labels and draw
    for x, y in enumerate(rotation):
        
        r_idx = x_to_r_index[facade_points_df.iloc[x]['x_axis_rotated'],facade_points_df.iloc[x]['y_axis_rotated']]
        s_idx = y_to_s_index[facade_points_df.iloc[x]['x_axis_rotated'],facade_points_df.iloc[x]['y_axis_rotated']]
        label = f"{letter_horizontal}{r_idx:02d}{letter_vertical}{s_idx:02d}"
        position = (facade_points_df.iloc[x]['x_axis'],facade_points_df.iloc[x]['y_axis'])
        cv2.putText(image, label, position, cv2.FONT_HERSHEY_PLAIN, 0.5, (100, 100, 100), 1)
        #cv2.circle(rotated, (x,y), radius=0, color=(0, 0, 255), thickness=3)

    if not auto_complete == 'yes':
        # Display the image
        cv2.imshow('Image with Custom Labels', image)
        #cv2.imwrite('HN05_Grid_Labels.png',rotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('south_building_facade_pixels_coordinates -Status: Done')

    #Add the Textual Numerical Nodes coordinates to the final DF
    #
    facade_points_df['letter_horizontal'] = letter_horizontal
    facade_points_df['coordinate_horizontal'] = x_to_r_index.values()
    facade_points_df['letter_vertical'] = letter_vertical
    facade_points_df['coordinate_vertical'] = y_to_s_index.values()

    return facade_points_df,tolerance_x,tolerance_y,y_threshold,n_save