#Importing usual libraries
import os, sys, datetime, argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd

#Import projects parameters
from functions.params import ROOT,PLAN_ROOT,PLAN_PNG,VISUALS

#Importing project functions
from functions.ROOM_NAMING.preprocessing_datasets_coordinates_rooms_full_coordinates_pixels import preprocessing_datasets_coordinates_rooms_full_coordinates_pixels
from functions.ROOM_NAMING.final_datasets_creation import final_datasets_creation
from functions.ROOM_NAMING.pixels_closest_neighbours import pixels_closest_neighbours
from functions.ROOM_NAMING.top_room_detection import top_room_detection
from functions.ROOM_NAMING.preprocessing_different_methods import preprocessing_different_methods
from functions.ROOM_NAMING.preprocessing_architectural_data import preprocessing_architectural_data
from functions.ROOM_NAMING.grand_finale_excel_table import grand_finale_excel_table
from functions.ROOM_NAMING.visualisation_rooms_names_and_position import visualisation_rooms_names_and_position
from functions.ROOM_NAMING.overall_hyperparameters_big_rooms_floors_computer_vision import overall_hyperparameters_big_rooms_floors_computer_vision
from functions.auto_complete_values import auto_complete_values

#Importing projects' support fuctions
from functions.validate_step import validate_step

#Uncomment the lines undertneath to be able to use variables into the script - Used in case of new plans/ rooms/ in the script

parser = argparse.ArgumentParser(description='Retrive, process, and save files manually downloaded from DWG TrueView.')
parser.add_argument('--floor', help='str. Building and floors. MUST be written like following: Building and floor. e.g. HS04', required=True, type=str)


args = parser.parse_args()

if __name__ == '__main__':

    floor = args.floor
    

    #df = pd.read_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'))

    #for index, row in df.iterrows():
    #    # Extract values from specific columns
    #    floor = row['floor']
    #    letter_horizontal = row['letter_horizontal']
    #    letter_vertical = row['letter_vertical']
    #    letter_horizontal_facade = row['letter_horizontal_facade']
    #    letter_vertical_facade = row['letter_vertical_facade']

    print(f'{floor} - Processing')
    auto_complete,x_auto,y_auto,angle1_auto,angle2_auto,min_size_trapeze_line_auto,angle_calculation_auto,area_threshold_auto,vertex_threshold_auto,number_false_room_auto,area_threshold_bigger_rooms_auto,bbox_area_auto,aspect_ratio_threshold_auto,balcony_area_detected_auto,number_false_room_transfer_auto,number_balcony_transfer_room_auto,angle_floor_auto,kernel_size_auto,tolerance_x_floor_auto,tolerance_y_floor_auto,y_threshold_floor_auto,a_index_floor_auto,angle_facade_auto,tolerance_x_facade_auto,tolerance_y_facade_auto,y_threshold_facade_auto,n_index_facade_auto,big_room_variable_auto = auto_complete_values(floor)

    rooms = preprocessing_architectural_data(floor)
    
    full_coordinates_pixels,CV_room_coordinates_top_left,floor_room_pixels_coordinates = preprocessing_datasets_coordinates_rooms_full_coordinates_pixels(floor,rooms)
    
    if auto_complete == 'yes':
        big_room_variable,FINAL_DF_CV_room_coordinates_top_left,big_size_rooms_and_pixels_coordinates = top_room_detection(floor,rooms,full_coordinates_pixels,CV_room_coordinates_top_left,auto_complete,big_room_variable_auto)
    else:
        while True:
            big_room_variable,FINAL_DF_CV_room_coordinates_top_left,big_size_rooms_and_pixels_coordinates = top_room_detection(floor,rooms,full_coordinates_pixels,CV_room_coordinates_top_left,auto_complete,big_room_variable_auto)
            if validate_step(top_room_detection):
                break
        
    one_coordinates_rooms, rooms_medium_size,room_CV_and_pixels_coordinates,medium_size_rooms_and_pixels_coordinates = preprocessing_different_methods(floor,rooms,FINAL_DF_CV_room_coordinates_top_left,big_room_variable,full_coordinates_pixels)
    
    FINAL_DF_CV_room_coordinates_top_left,FINAL_DF_room_and_inside_pixels_coordinates,DICT_full_room_association_to_ecb_names=final_datasets_creation(big_size_rooms_and_pixels_coordinates,CV_room_coordinates_top_left,full_coordinates_pixels,floor_room_pixels_coordinates,medium_size_rooms_and_pixels_coordinates,big_room_variable)
    
    FINAL_DF_distance_coordinates_list_one_coordinates,not_assigned_rooms_and_pixels_coordinates,DICT_full_room_association_to_ecb_names=pixels_closest_neighbours(floor,rooms,full_coordinates_pixels,DICT_full_room_association_to_ecb_names)
    
    grand_finale_excel_table(floor,DICT_full_room_association_to_ecb_names,CV_room_coordinates_top_left,not_assigned_rooms_and_pixels_coordinates)
    
    visualisation_rooms_names_and_position(floor,auto_complete,big_size_rooms_and_pixels_coordinates,FINAL_DF_room_and_inside_pixels_coordinates,FINAL_DF_distance_coordinates_list_one_coordinates,not_assigned_rooms_and_pixels_coordinates,FINAL_DF_CV_room_coordinates_top_left)

    overall_hyperparameters_big_rooms_floors_computer_vision(floor,big_room_variable)