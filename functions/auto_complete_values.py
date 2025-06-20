import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

import numpy as np
import pandas as pd

def auto_complete_values(floor):
    if os.path.exists(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv')):
        df = pd.read_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'))
        if df['floor'].isin([f'{floor}']).any():
            auto_complete=str(input(f"This floor already has been proceed. Do you wish to reuse the same values? (yes/no): ").strip().lower())
            #auto_complete = 'yes'
            if auto_complete == 'yes':
                variables = []
                for l in range(len(df.columns)):
                    for i in df[df['floor']==f'{floor}'].iterrows():
                        x = i[1][l]
                        variables.append(x)
                floor,letter_horizontal,letter_vertical,letter_horizontal_facade,letter_vertical_facade,x,y,angle1,angle2,min_size_trapeze_line,angle_calculation,area_threshold,vertex_threshold,number_false_room,area_threshold_bigger_rooms,bbox_area,aspect_ratio_threshold,balcony_area_detected,number_false_room_transfer,number_balcony_transfer_room,angle_floor,kernel_size,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor,angle_facade,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade,big_room_variable = variables
            else:
                #Creation of fake values to validatet the function
                variables = np.ones(32)
                auto_complete='no'
                floor,letter_horizontal,letter_vertical,letter_horizontal_facade,letter_vertical_facade,x,y,angle1,angle2,min_size_trapeze_line,angle_calculation,area_threshold,vertex_threshold,number_false_room,area_threshold_bigger_rooms,bbox_area,aspect_ratio_threshold,balcony_area_detected,number_false_room_transfer,number_balcony_transfer_room,angle_floor,kernel_size,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor,angle_facade,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade,big_room_variable = variables
        else:
            variables = np.ones(32)
            auto_complete='no'
            floor,letter_horizontal,letter_vertical,letter_horizontal_facade,letter_vertical_facade,x,y,angle1,angle2,min_size_trapeze_line,angle_calculation,area_threshold,vertex_threshold,number_false_room,area_threshold_bigger_rooms,bbox_area,aspect_ratio_threshold,balcony_area_detected,number_false_room_transfer,number_balcony_transfer_room,angle_floor,kernel_size,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor,angle_facade,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade,big_room_variable = variables
    else:
        variables = np.ones(32)
        auto_complete='no'
        floor,letter_horizontal,letter_vertical,letter_horizontal_facade,letter_vertical_facade,x,y,angle1,angle2,min_size_trapeze_line,angle_calculation,area_threshold,vertex_threshold,number_false_room,area_threshold_bigger_rooms,bbox_area,aspect_ratio_threshold,balcony_area_detected,number_false_room_transfer,number_balcony_transfer_room,angle_floor,kernel_size,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor,angle_facade,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade,big_room_variable = variables
            
    return auto_complete,x,y,angle1,angle2,min_size_trapeze_line,angle_calculation,area_threshold,vertex_threshold,number_false_room,area_threshold_bigger_rooms,bbox_area,aspect_ratio_threshold,balcony_area_detected,number_false_room_transfer,number_balcony_transfer_room,angle_floor,kernel_size,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor,angle_facade,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade,big_room_variable

            