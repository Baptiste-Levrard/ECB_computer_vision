import os, sys, datetime, argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np

#Import projects parameters
from functions.params import ROOT,PLAN_ROOT,PLAN_PNG,VISUALS

def overall_hyperparameters_floors_computer_vision(floor,letter_horizontal,letter_vertical,letter_horizontal_facade,letter_vertical_facade,angle1,angle2,min_size_trapeze_line,x,y,angle_calculation,area_threshold,vertex_threshold,number_false_room,area_threshold_bigger_rooms,bbox_area,aspect_ratio_threshold,balcony_area_detected,number_false_room_transfer,number_balcony_transfer_room,angle_floor,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor,angle_facade,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade,kernel_size):
    '''
    Save and create a CSV file, in the VISUALS folder, that contain all the hyperparameters associated to the floor.
    floor=str
    letter_horizontal=str
    letter_vertical=str
    letter_horizontal_facade=str
    letter_vertical_facade=str
    angle1=float
    angle2=float
    min_size_trapeze_line=int
    x=int
    y=int
    angle_calculation=int
    area_threshold=float
    vertex_threshold=int
    number_false_room=int
    area_threshold_bigger_rooms=int
    bbox_area=float
    aspect_ratio_threshold=float
    balcony_area_detected=int
    number_false_room_transfer=int
    number_balcony_transfer_room=int
    angle_floor=int
    tolerance_x_floor=int,
    tolerance_y_floor=int
    y_threshold_floor=int
    a_index_floor=int
    angle_facade=float
    tolerance_x_facade=int
    tolerance_y_facade=int
    y_threshold_facade=int
    n_index_facade=int
    return
    df=DataFrame
    '''
    if not os.path.exists(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv')):
        temps1 = pd.DataFrame(columns=[
                    'floor',
                    'letter_horizontal',
                    'letter_vertical',
                    'letter_horizontal_facade',
                    'letter_vertical_facade',
                    'horizontal_pixel_max',
                    'vertical_pixel_max',
                    'angle1',
                    'angle2',
                    'min_size_trapeze_line',
                    'angle_calculation',
                    'area_threshold',
                    'vertex_threshold',
                    'number_false_room',
                    'area_threshold_bigger_rooms',
                    'bbox_area',
                    'aspect_ratio_threshold',
                    'balcony_area_detected',
                    'number_false_room_transfer',
                    'number_balcony_transfer_room',
                    'angle_floor',
                    'kernel_size',
                    'tolerance_x_floor',
                    'tolerance_y_floor',
                    'y_threshold_floor',
                    'horizontal_index_floor',
                    'angle_facade',
                    'tolerance_x_facade',
                    'tolerance_y_facade',
                    'y_threshold_facade',
                    'horizontal_index_facade'])
        temps1.to_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'), index=False)
        temp = pd.DataFrame(
                {
                    'floor':floor,
                    'letter_horizontal': letter_horizontal,
                    'letter_vertical': letter_vertical,
                    'letter_horizontal_facade': letter_horizontal_facade,
                    'letter_vertical_facade': letter_vertical_facade,
                    'horizontal_pixel_max': x,
                    'vertical_pixel_max': y,
                    'angle1':angle1,
                    'angle2':angle2,
                    'min_size_trapeze_line':min_size_trapeze_line,
                    'angle_calculation':angle_calculation,
                    'area_threshold':area_threshold,
                    'vertex_threshold':vertex_threshold,
                    'number_false_room':number_false_room,
                    'area_threshold_bigger_rooms': area_threshold_bigger_rooms,
                    'bbox_area': bbox_area,
                    'aspect_ratio_threshold':aspect_ratio_threshold,
                    'balcony_area_detected':balcony_area_detected,
                    'number_false_room_transfer':number_false_room_transfer,
                    'number_balcony_transfer_room':number_balcony_transfer_room,
                    'angle_floor':angle_floor,
                    'kernel_size':kernel_size,
                    'tolerance_x_floor':tolerance_x_floor,
                    'tolerance_y_floor':tolerance_y_floor,
                    'y_threshold_floor':y_threshold_floor,
                    'horizontal_index_floor':a_index_floor,
                    'angle_facade':angle_facade,
                    'tolerance_x_facade':tolerance_x_facade,
                    'tolerance_y_facade':tolerance_y_facade,
                    'y_threshold_facade':y_threshold_facade,
                    'horizontal_index_facade':n_index_facade
                },index=[0]
            )
        df = pd.concat([temps1, temp], ignore_index=True)
        df.to_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'), index=False)
        print('overall_hyperparameters_floors_computer_vision.csv has been created')
    else:
        df = pd.read_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'))
        out = df['floor'].eq(f'{floor}').any()
        if out == np.False_:
            temp = pd.DataFrame(
                {
                    'floor':floor,
                    'letter_horizontal': letter_horizontal,
                    'letter_vertical': letter_vertical,
                    'letter_horizontal_facade': letter_horizontal_facade,
                    'letter_vertical_facade': letter_vertical_facade,
                    'horizontal_pixel_max': x,
                    'vertical_pixel_max': y,
                    'angle1':angle1,
                    'angle2':angle2,
                    'min_size_trapeze_line':min_size_trapeze_line,
                    'angle_calculation':angle_calculation,
                    'area_threshold':area_threshold,
                    'vertex_threshold':vertex_threshold,
                    'number_false_room':number_false_room,
                    'area_threshold_bigger_rooms':area_threshold_bigger_rooms,
                    'bbox_area': bbox_area,
                    'aspect_ratio_threshold':aspect_ratio_threshold,
                    'balcony_area_detected':balcony_area_detected,
                    'number_false_room_transfer':number_false_room_transfer,
                    'number_balcony_transfer_room':number_balcony_transfer_room,
                    'angle_floor':angle_floor,
                    'kernel_size':kernel_size,
                    'tolerance_x_floor':tolerance_x_floor,
                    'tolerance_y_floor':tolerance_y_floor,
                    'y_threshold_floor':y_threshold_floor,
                    'horizontal_index_floor':a_index_floor,
                    'angle_facade':angle_facade,
                    'tolerance_x_facade':tolerance_x_facade,
                    'tolerance_y_facade':tolerance_y_facade,
                    'y_threshold_facade':y_threshold_facade,
                    'horizontal_index_facade':n_index_facade
                },index=[0]
            )
            df = pd.concat([df, temp], ignore_index=True)
            df.to_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'), index=False)
            print('overall_hyperparameters_floors_computer_vision.csv has been updated')
        else:
            temp = pd.DataFrame(
                {
                    'floor':floor,
                    'letter_horizontal': letter_horizontal,
                    'letter_vertical': letter_vertical,
                    'letter_horizontal_facade': letter_horizontal_facade,
                    'letter_vertical_facade': letter_vertical_facade,
                    'horizontal_pixel_max': x,
                    'vertical_pixel_max': y,
                    'angle1':angle1,
                    'angle2':angle2,
                    'min_size_trapeze_line':min_size_trapeze_line,
                    'angle_calculation':angle_calculation,
                    'area_threshold':area_threshold,
                    'vertex_threshold':vertex_threshold,
                    'number_false_room':number_false_room,
                    'area_threshold_bigger_rooms':area_threshold_bigger_rooms,
                    'bbox_area': bbox_area,
                    'aspect_ratio_threshold':aspect_ratio_threshold,
                    'balcony_area_detected':balcony_area_detected,
                    'number_false_room_transfer':number_false_room_transfer,
                    'number_balcony_transfer_room':number_balcony_transfer_room,
                    'angle_floor':angle_floor,
                    'kernel_size':kernel_size,
                    'tolerance_x_floor':tolerance_x_floor,
                    'tolerance_y_floor':tolerance_y_floor,
                    'y_threshold_floor':y_threshold_floor,
                    'horizontal_index_floor':a_index_floor,
                    'angle_facade':angle_facade,
                    'tolerance_x_facade':tolerance_x_facade,
                    'tolerance_y_facade':tolerance_y_facade,
                    'y_threshold_facade':y_threshold_facade,
                    'horizontal_index_facade':n_index_facade
                },index=[0]
            )
            df = df[df['floor'] != floor]
            df = pd.concat([df, temp], ignore_index=True)
            df.to_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'), index=False)
            print('overall_hyperparameters_floors_computer_vision.csv has been updated')
    return df