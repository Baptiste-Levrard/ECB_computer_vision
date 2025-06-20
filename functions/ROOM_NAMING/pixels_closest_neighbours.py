import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

import cv2
import numpy as np
import pandas as pd
import math
import pickle

def pixels_closest_neighbours(floor,rooms,full_coordinates_pixels,DICT_full_room_association_to_ecb_names):
    """
    Function calculate the euclidan distance between Coordinates of rooms <2 sqm2 and CV detected rooms non affiliated yet.
    
    Input:
    floor=str. The floor used for the script. Must be spelled HN05 or HS04...
    rooms= DF. Preprocessed ECB rooms names
    full_coordinates_pixels= DF 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. Full DF of the coordinates of the floor
    DICT_full_room_association_to_ecb_names= Dict. Coordinates of ECB rooms and CV coordinates rooms - Same line, same supposed room

    Output
    FINAL_DF_distance_coordinates_list_one_coordinates=DF 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. One coordinates non attributed rooms
    not_assigned_rooms_and_pixels_coordinates= DICT. two columns - One for the index, the other one for the Coordinate
    
    """
    
    with open(os.path.join(os.getcwd(),VISUALS, f'{floor}', f'{floor}_room_pixels.pkl'),'rb') as f:
        room_pixels = pickle.load(f)
    
    #Could be merged in a single nested for loop.
    DICT_non_matching_CV_room_and_room_names_ECB = {}
    for i in room_pixels.keys():
        if i not in DICT_full_room_association_to_ecb_names.keys():
            DICT_non_matching_CV_room_and_room_names_ECB[i]= np.nan
    
    DICT_non_matching_CV_room_and_room_names_ECB_centroide_pixels = {}
    for i in DICT_non_matching_CV_room_and_room_names_ECB:
        sum_x = sum(pixel[0] for pixel in room_pixels[i])
        sum_y = sum(pixel[1] for pixel in room_pixels[i])
        centroid_x = sum_x / len(room_pixels[i])
        centroid_y = sum_y / len(room_pixels[i])
        DICT_non_matching_CV_room_and_room_names_ECB_centroide_pixels[i] = (round(centroid_x),round(centroid_y))

    ##Reuse this method to get only the values that are not used
    ##Should be a value that always get updated

    not_assigned_rooms_and_pixels_coordinates = pd.merge(rooms[~rooms['coordinates_ECB_space'].isin(DICT_full_room_association_to_ecb_names.values())],full_coordinates_pixels,how="inner",on=["coordinates_ECB_space", "coordinates_ECB_space"])
    not_assigned_rooms_and_pixels_coordinates['target_pixels'] = list(zip(not_assigned_rooms_and_pixels_coordinates['x_axis'], not_assigned_rooms_and_pixels_coordinates['y_axis']))


    #Creation of two dictionnaries that will hold as keys MY rooms, and as values - distance_list: distances between my pixels coordinates and the ECB coordinates. distance_coordinates_list: the ECB coordinates affiliated
    #Theory; will be used to affialiate the rooms that don't have any rooms_coordinates in their pixels areas.
    #Simple Euclidian Distance
    distance_list_one_coordinates = {}
    distance_coordinates_list_one_coordinates = {}
    for i in DICT_non_matching_CV_room_and_room_names_ECB_centroide_pixels:
        distance_list_one_coordinates[i]= np.inf
        distance_coordinates_list_one_coordinates[i] = np.nan
        for j in range(len(not_assigned_rooms_and_pixels_coordinates['target_pixels'])):
            if not_assigned_rooms_and_pixels_coordinates['coordinates_ECB_space'][j] in ('A21Q06', 'A21Q08', 'A29Q06', 'A32Q07'):
                pass
            else:
                dx2 = (not_assigned_rooms_and_pixels_coordinates['target_pixels'][j][0]-DICT_non_matching_CV_room_and_room_names_ECB_centroide_pixels[i][1])**2          # (200-10)^2
                dy2 = (not_assigned_rooms_and_pixels_coordinates['target_pixels'][j][1]-DICT_non_matching_CV_room_and_room_names_ECB_centroide_pixels[i][0])**2
                distance = math.sqrt(dx2 + dy2)
                if distance_list_one_coordinates[i] > distance:
                    distance_list_one_coordinates[i] = distance 
                    distance_coordinates_list_one_coordinates[i] = not_assigned_rooms_and_pixels_coordinates['coordinates_ECB_space'][j]


    DF_distance_coordinates_list_one_coordinates = pd.DataFrame.from_dict(distance_coordinates_list_one_coordinates, orient='index', columns=['coordinates_ECB_space'])
    DF_distance_coordinates_list_one_coordinates = DF_distance_coordinates_list_one_coordinates.reset_index()
    FINAL_DF_distance_coordinates_list_one_coordinates = pd.merge(DF_distance_coordinates_list_one_coordinates, full_coordinates_pixels,how="inner",on=["coordinates_ECB_space", "coordinates_ECB_space"])

    not_assigned_rooms_and_pixels_coordinates = not_assigned_rooms_and_pixels_coordinates[~not_assigned_rooms_and_pixels_coordinates['coordinates_ECB_space'].isin(FINAL_DF_distance_coordinates_list_one_coordinates['coordinates_ECB_space'])]

    DICT_full_room_association_to_ecb_names.update(distance_coordinates_list_one_coordinates)

    print('pixels_closest_neighbours -Status: Done')
    
    return FINAL_DF_distance_coordinates_list_one_coordinates,not_assigned_rooms_and_pixels_coordinates,DICT_full_room_association_to_ecb_names