import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

import pandas as pd

def preprocessing_different_methods(floor,rooms,FINAL_DF_CV_room_coordinates_top_left,big_room_variable,full_coordinates_pixels):
    '''
    Compute the DataFrame of one coordinates rooms (Less than 2 sqm2), rooms bigger than 2sqm2 but not in the biggest rooms.

    Input
    floor=str. The floor used for the script. Must be spelled HN05 or HS04...
    rooms= DF. Preprocessed ECB rooms names
    FINAL_DF_CV_room_coordinates_top_left: DF. 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. DF of the CV detected rooms and there TOP left coordinates and pixels position.
    big_room_variable= int. Number of rooms that are big enough to have their size aligned with the ECB size.
    full_coordinates_pixels: DF 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. Full DF of the coordinates of the floor

    Output
    one_coordinates_rooms= ditc. Two columns; The index of the position of the room and it's coordinates
    rooms_medium_size= df. Coordinates of the ECB plans
    room_CV_and_pixels_coordinates=DF 3 main columns [target_pixels], [x_axis], [y_axis]. Coordinates of the rooms
    medium_size_rooms_and_pixels_coordinates=DF 3 main columns [target_pixels], [x_axis], [y_axis]. Coordinates of the rooms, medium rooms.
    
    '''
    ##Rooms that are less than 2sqm
    one_coordinates_rooms = rooms[rooms['SP_Dimension Net']<3]
    one_coordinates_rooms_and_pixels_coordinates = pd.merge(one_coordinates_rooms, full_coordinates_pixels,how="inner",on=["coordinates_ECB_space", "coordinates_ECB_space"])
    one_coordinates_rooms_and_pixels_coordinates['target_pixels']= list(zip(one_coordinates_rooms_and_pixels_coordinates['x_axis'], one_coordinates_rooms_and_pixels_coordinates['y_axis']))

    #Rest of the room (not Top area rooms, not sqm2 <2)
    rest_rooms=rooms[big_room_variable:]
    rooms_medium_size = rest_rooms[rest_rooms['SP_Dimension Net']>3]

    medium_size_rooms_and_pixels_coordinates = pd.merge(rooms_medium_size,full_coordinates_pixels,how="inner",on=["coordinates_ECB_space", "coordinates_ECB_space"])
    room_CV_and_pixels_coordinates = FINAL_DF_CV_room_coordinates_top_left[big_room_variable:] #Should be in a previous variable for an easier access
    medium_size_rooms_and_pixels_coordinates['target_pixels']= list(zip(medium_size_rooms_and_pixels_coordinates['x_axis'], medium_size_rooms_and_pixels_coordinates['y_axis']))
    room_CV_and_pixels_coordinates['target_pixels']=list(zip(room_CV_and_pixels_coordinates['x_axis'], room_CV_and_pixels_coordinates['y_axis']))

    print('preprocessing_different_methods -Status: Done')

    return one_coordinates_rooms, rooms_medium_size,room_CV_and_pixels_coordinates,medium_size_rooms_and_pixels_coordinates