import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

import pandas as pd
import math


def final_datasets_creation(big_size_rooms_and_pixels_coordinates,CV_room_coordinates_top_left,full_coordinates_pixels,floor_room_pixels_coordinates,medium_size_rooms_and_pixels_coordinates,big_room_variable):
    """
    Might be a language abuse of the term -final- in this case it s a datasets lists (Adding the pixels coordinates for plotting in visualisation part)
    Inputs:
    big_size_rooms_and_pixels_coordinates: dict. two columns - One for the index, the other one for the Coordinate
    CV_room_coordinates_top_left: dict. two columns - One for the index, the other one for the Coordinate
    full_coordinates_pixels: DF 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. Full DF of the coordinates of the floor
    floor_room_pixels_coordinates : DF 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. DF of the coordinates extarcted of the ECB's rooms name.
    medium_size_rooms_and_pixels_coordinates: DF 1 main column [coordinates_ECB_space]. DF of pixels coordinates of the rooms that less than the top delimitated and higher than 2 sqm2

    Output:
    FINAL_DF_CV_room_coordinates_top_left: DF. 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. DF of the CV detected rooms and there TOP left coordinates and pixels position.
    FINAL_DF_room_and_inside_pixels_coordinates: DF. 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. DF of pixels coordinates of the medium rooms - Lesser than the top manually decided rooms and higher than the 2 sqm2
    DICT_full_room_association_to_ecb_names: Dict. Coordinates of ECB rooms and CV coordinates rooms - Same line, same supposed room
    """
    ## Final 
    DF_CV_room_coordinates_top_left = pd.DataFrame.from_dict(CV_room_coordinates_top_left, orient='index', columns=['coordinates_ECB_space'])
    DF_CV_room_coordinates_top_left = DF_CV_room_coordinates_top_left.reset_index()
    FINAL_DF_CV_room_coordinates_top_left = pd.merge(DF_CV_room_coordinates_top_left, full_coordinates_pixels,how="inner",on=["coordinates_ECB_space", "coordinates_ECB_space"])
    
    # Iteration over the coordinates associated with a CV detected room. Match the room with names of of ECB rooms if detected
    non_matching_CV_room_and_room_names_ECB = []
    matching_CV_room_and_room_names_ECB = {}
    for i in sorted(floor_room_pixels_coordinates['room'].unique())[big_room_variable:]:
        for j in floor_room_pixels_coordinates[floor_room_pixels_coordinates['room']==i]['coordinates_ECB_space']:
            if j in medium_size_rooms_and_pixels_coordinates['coordinates_ECB_space'].values:
            #Before applying this Coordinate to this CV room, Check if the room doesn't already have an coordinate linked to it. 
                if matching_CV_room_and_room_names_ECB.get(i):
                    #If a coordinate is already linked to the CV room, calculate the distance from the previously determined top left coordinate of the CV room and the two conflictiong coordinates
                    #x and y axis of the coordinates of the callenging room for the CV coordinates
                    dx2_distance1 = (FINAL_DF_CV_room_coordinates_top_left[FINAL_DF_CV_room_coordinates_top_left['index']==i]['x_axis'].iloc[0]-floor_room_pixels_coordinates[floor_room_pixels_coordinates['coordinates_ECB_space']==j]['x_axis'].iloc[0])**2          # (200-10)^2
                    dy2_distance1 = (FINAL_DF_CV_room_coordinates_top_left[FINAL_DF_CV_room_coordinates_top_left['index']==i]['y_axis'].iloc[0]-floor_room_pixels_coordinates[floor_room_pixels_coordinates['coordinates_ECB_space']==j]['x_axis'].iloc[0])**2
                    distance1 = math.sqrt(dx2_distance1 + dy2_distance1)
                    
                    #x and y axis of the coordinates of the room, already validated coordinate of the room for the CV room number
                    dx2_distance2 = (FINAL_DF_CV_room_coordinates_top_left[FINAL_DF_CV_room_coordinates_top_left['index']==i]['x_axis'].iloc[0]-floor_room_pixels_coordinates[floor_room_pixels_coordinates['coordinates_ECB_space']==matching_CV_room_and_room_names_ECB[i]]['x_axis'].iloc[0])**2         
                    dy2_distance2 = (FINAL_DF_CV_room_coordinates_top_left[FINAL_DF_CV_room_coordinates_top_left['index']==i]['x_axis'].iloc[0]-floor_room_pixels_coordinates[floor_room_pixels_coordinates['coordinates_ECB_space']==matching_CV_room_and_room_names_ECB[i]]['y_axis'].iloc[0])**2
                    distance2 = math.sqrt(dx2_distance2 + dy2_distance2)
    
                    #If the new coordinate distance with the top left coordinate is smaller than the previous coordinate to the top left coordinate then replace it
                    if distance1 < distance2:
                        matching_CV_room_and_room_names_ECB[i]=j
                    else:
                        pass
                else:
                    matching_CV_room_and_room_names_ECB[i]=j
            else:
                pass
        try: 
            matching_CV_room_and_room_names_ECB[i]==None
        except:
            non_matching_CV_room_and_room_names_ECB.append(i)
    
    DF_matching_CV_room_and_room_names_ECB = pd.DataFrame.from_dict(matching_CV_room_and_room_names_ECB, orient='index', columns=['coordinates_ECB_space'])
    DF_matching_CV_room_and_room_names_ECB = DF_matching_CV_room_and_room_names_ECB.reset_index()
    FINAL_DF_room_and_inside_pixels_coordinates = pd.merge(DF_matching_CV_room_and_room_names_ECB, full_coordinates_pixels,how="inner",on=["coordinates_ECB_space", "coordinates_ECB_space"])
    
    DICT_full_room_association_to_ecb_names = dict(zip(sorted(floor_room_pixels_coordinates['room'].unique())[:big_room_variable],big_size_rooms_and_pixels_coordinates.sort_values(by=['SP_Dimension Net'],ascending=False)['coordinates_ECB_space']))
    DICT_full_room_association_to_ecb_names.update(matching_CV_room_and_room_names_ECB)

    print('final_datasets_creation -Status: Done')

    return FINAL_DF_CV_room_coordinates_top_left,FINAL_DF_room_and_inside_pixels_coordinates,DICT_full_room_association_to_ecb_names