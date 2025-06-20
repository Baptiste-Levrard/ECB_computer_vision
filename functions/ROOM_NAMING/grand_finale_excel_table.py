import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

import pandas as pd

def grand_finale_excel_table(floor,DICT_full_room_association_to_ecb_names,CV_room_coordinates_top_left,not_assigned_rooms_and_pixels_coordinates):
    '''
    Compute a single file of the association of ECB current names and CV detected names.
    
    Input
    floor=str. The floor used for the script. Must be spelled HN05 or HS04...
    DICT_full_room_association_to_ecb_names = Dict. Coordinates of ECB rooms and CV coordinates rooms - Same line, same supposed room
    CV_room_coordinates_top_left= dict. two columns - One for the index, the other one for the Coordinate
    
    Output
    Save the computed DF in the corresponding floor folder as a {floor}_rooms_coordinates_dictionnary.csv
    '''
    rooms_coordinates_dictionnary = pd.concat([pd.DataFrame.from_dict(DICT_full_room_association_to_ecb_names, orient='index', columns=['ecb_names']), pd.DataFrame.from_dict(CV_room_coordinates_top_left, orient='index', columns=['baptiste_room_coordinates'])], axis=1)
    not_assigned_rooms_and_pixels_coordinates['ecb_names']=not_assigned_rooms_and_pixels_coordinates['coordinates_ECB_space']
    not_assigned_rooms_and_pixels_coordinates['one_room_coordinate_supposed']='deducted_one_room'
    rooms_coordinates_dictionnary = pd.concat([rooms_coordinates_dictionnary,pd.DataFrame(not_assigned_rooms_and_pixels_coordinates[['ecb_names','one_room_coordinate_supposed']]).set_index(pd.Index(range(100-len(not_assigned_rooms_and_pixels_coordinates), (100-len(not_assigned_rooms_and_pixels_coordinates)) + len(not_assigned_rooms_and_pixels_coordinates),1)))])
    rooms_coordinates_dictionnary.to_csv(os.path.join(os.getcwd(), VISUALS ,f'{floor}', f'{floor}_rooms_coordinates_dictionnary.csv'),index=True)

    print('grand_finale_excel_table -Status: Done')
    
    return rooms_coordinates_dictionnary,not_assigned_rooms_and_pixels_coordinates