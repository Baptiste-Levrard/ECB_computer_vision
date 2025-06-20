#Importing usual libraries
import os, sys, datetime, argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd

#Import projects parameters
from functions.params import ROOT,PLAN_ROOT,PLAN_PNG,VISUALS

#Importing project functions
from functions.auto_complete_values import auto_complete_values
from functions.retrieve_pdf import retrieve_pdf
from functions.rotate_png import rotate_png
from functions.resize_image import resize_image
from functions.crop_plan import crop_plan
from functions.rooms_contours import rooms_contours
from functions.transfer_grid import transfer_grid
from functions.trapezes_lines_facade_plan import trapezes_lines_facade_plan
from functions.floor_nodes_detections import floor_nodes_detections
from functions.facade_nodes_detections import facade_nodes_detections
from functions.nodes_detection import nodes_detection
from functions.divided_nodes_by_floor_position import divided_nodes_by_floor_position
from functions.north_building_floor_pixels_coordinates import north_building_floor_pixels_coordinates
from functions.north_building_facade_pixels_coordinates import north_building_facade_pixels_coordinates
from functions.south_building_floor_pixels_coordinates import south_building_floor_pixels_coordinates
from functions.south_building_facade_pixels_coordinates import south_building_facade_pixels_coordinates
from functions.pixels_matching import pixels_matching
from functions.visualisation_3D_maps import visualisation_3D_maps
from functions.overall_hyperparameters_floors_computer_vision import overall_hyperparameters_floors_computer_vision
from functions.image_rotation import image_rotation


#Importing projects' support fuctions
from functions.rotate_points_with_cv2 import rotate_points_with_cv2
from functions.pixel_matching_support_functions import *
from functions.validate_step import validate_step

#Uncomment the lines undertneath to be able to use variables into the script - Used in case of new plans/ rooms/ in the script

parser = argparse.ArgumentParser(description='Retrive, process, and save files manually downloaded from DWG TrueView.')
parser.add_argument('--floor', help='str. Building and floors. MUST be written like following: Building and floor. e.g. HS04', required=True, type=str)
parser.add_argument('--letter_horizontal', help='str. Buildings axis letter.',required=True, type=str)
parser.add_argument('--letter_vertical', help='str. Buildings axis letter.',required=True, type=str)
parser.add_argument('--letter_horizontal_facade', help='str. Buildings axis letter.',required=True, type=str)
parser.add_argument('--letter_vertical_facade', help='str. Buildings axis letter.',required=True, type=str)

args = parser.parse_args()

if __name__ == '__main__':

    floor = args.floor
    letter_horizontal = args.letter_horizontal
    letter_vertical = args.letter_vertical
    letter_horizontal_facade = args.letter_horizontal_facade
    letter_vertical_facade = args.letter_vertical_facade

#Those commented lines underneath are made to make the project run over all the floors faster. Instead of manually input the variables, 
#    df = pd.read_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'))
    
#    for index, row in df.iterrows():
#        # Extract values from specific columns
#        floor = row['floor']
#        letter_horizontal = row['letter_horizontal']
#        letter_vertical = row['letter_vertical']
#        letter_horizontal_facade = row['letter_horizontal_facade']
#        letter_vertical_facade = row['letter_vertical_facade']
    
        auto_complete,x_auto,y_auto,angle1_auto,angle2_auto,min_size_trapeze_line_auto,angle_calculation_auto,area_threshold_auto,vertex_threshold_auto,number_false_room_auto,area_threshold_bigger_rooms_auto,bbox_area_auto,aspect_ratio_threshold_auto,balcony_area_detected_auto,number_false_room_transfer_auto,number_balcony_transfer_room_auto,angle_floor_auto,kernel_size_auto,tolerance_x_floor_auto,tolerance_y_floor_auto,y_threshold_floor_auto,a_index_floor_auto,angle_facade_auto,tolerance_x_facade_auto,tolerance_y_facade_auto,y_threshold_facade_auto,n_index_facade_auto,big_room_variable = auto_complete_values(floor)
        
        print(f'Initiating - {floor} - architectural plans pre-processing')
        ###
        ###
        ###
        plan,grid = retrieve_pdf(floor)
        ###
        ###
        ###
        plan_rotated,grid_rotated = rotate_png(auto_complete,plan,grid)
        ###
        ###
        ###
        if auto_complete == 'yes':
            original_points,angle1,angle2,min_size_trapeze_line = trapezes_lines_facade_plan(grid_rotated,auto_complete,angle1_auto,angle2_auto,min_size_trapeze_line_auto)
            plan_resized, grid_resized,resized_point1,resized_point2,resized_point3,resized_point4,x,y = resize_image(plan_rotated,grid_rotated,original_points,auto_complete ,x_auto,y_auto)
        else:
            while True:
                original_points,angle1,angle2,min_size_trapeze_line = trapezes_lines_facade_plan(grid_rotated,auto_complete,angle1_auto,angle2_auto,min_size_trapeze_line_auto)
                plan_resized, grid_resized,resized_point1,resized_point2,resized_point3,resized_point4,x,y = resize_image(plan_rotated,grid_rotated,original_points,auto_complete ,x_auto,y_auto)
                if validate_step(trapezes_lines_facade_plan):
                    break
        ###
        ###
        ###
        if auto_complete == 'yes':
           plan_rotated,grid_rotated,points_rotated,angle_calculation = image_rotation(plan_resized,grid_resized,resized_point1,resized_point2,resized_point3,resized_point4,auto_complete,angle_calculation_auto)
        else:
            while True:
                plan_rotated,grid_rotated,points_rotated,angle_calculation = image_rotation(plan_resized,grid_resized,resized_point1,resized_point2,resized_point3,resized_point4,auto_complete,angle_calculation_auto)
                if validate_step(image_rotation):
                    break
        ###
        ###
        ###
        plan_cropped,grid_cropped,new_resized_point1,new_resized_point2,new_resized_point3,new_resized_point4 = crop_plan(auto_complete,plan_rotated,grid_rotated,floor,points_rotated[0],points_rotated[1],points_rotated[2],points_rotated[3])
        ###
        ###
        ###
        nodes = nodes_detection(auto_complete,grid_cropped,floor)
        ###
        ###
        ###
        if auto_complete == 'yes':
            black_background,centroides_y_values,centroides_x_values,sorted_contours,room_pixels,sorted_centroides_y,area_threshold,vertex_threshold,number_false_room,area_threshold_bigger_rooms,bbox_area,aspect_ratio_threshold,balcony_area_detected = rooms_contours(plan_cropped,floor,auto_complete,area_threshold_auto,vertex_threshold_auto,number_false_room_auto,area_threshold_bigger_rooms_auto,bbox_area_auto,aspect_ratio_threshold_auto,balcony_area_detected_auto)
        else:
            while True:
                black_background,centroides_y_values,centroides_x_values,sorted_contours,room_pixels,sorted_centroides_y,area_threshold,vertex_threshold,number_false_room,area_threshold_bigger_rooms,bbox_area,aspect_ratio_threshold,balcony_area_detected = rooms_contours(plan_cropped,floor,auto_complete,area_threshold_auto,vertex_threshold_auto,number_false_room_auto,area_threshold_bigger_rooms_auto,bbox_area_auto,aspect_ratio_threshold_auto,balcony_area_detected_auto)
                if validate_step(rooms_contours):
                    break
        ###
        ###
        ###
        floor_string =visualisation_3D_maps(room_pixels,floor,area_threshold,vertex_threshold,number_false_room,bbox_area,aspect_ratio_threshold,angle_calculation,area_threshold_bigger_rooms,balcony_area_detected)
        ###
        ###
        ###
        if auto_complete == 'yes':
            floor_shape,grid_transfer,nodes,number_false_room_transfer,number_balcony_transfer_room=transfer_grid(floor,angle_calculation,auto_complete,number_false_room_transfer_auto,number_balcony_transfer_room_auto)
        else:
            while True:
                floor_shape,grid_transfer,nodes,number_false_room_transfer,number_balcony_transfer_room=transfer_grid(floor,angle_calculation,auto_complete,number_false_room_transfer_auto,number_balcony_transfer_room_auto)
                if validate_step(transfer_grid):
                    break
        ###
        ###
        ###
        if 'HN' in floor:
            if auto_complete == 'yes':
                floor_points,floor_points_rotated_back,angle_floor_rotation,kernel_size,cXorient_floor, cYorient_floor,h_floor, w_floor = floor_nodes_detections(grid_transfer,floor,new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2,black_background,auto_complete ,angle_floor_auto,kernel_size_auto)
                floor_points_df,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor = north_building_floor_pixels_coordinates(floor,letter_horizontal,letter_vertical,floor_points,floor_points_rotated_back,angle_floor_rotation,cXorient_floor, cYorient_floor,h_floor, w_floor,auto_complete ,tolerance_x_floor_auto,tolerance_y_floor_auto,y_threshold_floor_auto,a_index_floor_auto)
            else:
                while True:
                    floor_points,floor_points_rotated_back,angle_floor_rotation,kernel_size,cXorient_floor, cYorient_floor,h_floor, w_floor = floor_nodes_detections(grid_transfer,floor,new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2,black_background,auto_complete ,angle_floor_auto,kernel_size_auto)
                    floor_points_df,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor = north_building_floor_pixels_coordinates(floor,letter_horizontal,letter_vertical,floor_points,floor_points_rotated_back,angle_floor_rotation,cXorient_floor, cYorient_floor,h_floor, w_floor,auto_complete ,tolerance_x_floor_auto,tolerance_y_floor_auto,y_threshold_floor_auto,a_index_floor_auto)
                    if validate_step(north_building_floor_pixels_coordinates):
                        break
        elif 'HS' in floor:
            if auto_complete == 'yes':
                floor_points,floor_points_rotated_back,angle_floor_rotation,kernel_size,cXorient_floor, cYorient_floor,h_floor, w_floor = floor_nodes_detections(grid_transfer,floor,new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2,black_background,auto_complete ,angle_floor_auto,kernel_size_auto)
                floor_points_df,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor=south_building_floor_pixels_coordinates(floor,letter_horizontal,letter_vertical,floor_points,floor_points_rotated_back,angle_floor_rotation,cXorient_floor, cYorient_floor,h_floor, w_floor,auto_complete,tolerance_x_floor_auto,tolerance_y_floor_auto,y_threshold_floor_auto,a_index_floor_auto)
            else:
                while True:
                    floor_points,floor_points_rotated_back,angle_floor_rotation,kernel_size,cXorient_floor, cYorient_floor,h_floor, w_floor = floor_nodes_detections(grid_transfer,floor,new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2,black_background,auto_complete ,angle_floor_auto,kernel_size_auto)
                    floor_points_df,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor=south_building_floor_pixels_coordinates(floor,letter_horizontal,letter_vertical,floor_points,floor_points_rotated_back,angle_floor_rotation,cXorient_floor, cYorient_floor,h_floor, w_floor,auto_complete,tolerance_x_floor_auto,tolerance_y_floor_auto,y_threshold_floor_auto,a_index_floor_auto)
                    if validate_step(south_building_floor_pixels_coordinates):
                        break
                                 
        ###
        ###
        ###
        if 'HN' in floor:
            if auto_complete == 'yes':
                facade_points,facade_points_rotated_back,angle_facade_rotation,cXorient_facade, cYorient_facade,h_facade, w_facade = facade_nodes_detections(grid_cropped,floor,new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2,black_background,auto_complete ,angle_facade_auto)
                facade_points_df,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade = north_building_facade_pixels_coordinates(floor,letter_horizontal_facade,letter_vertical_facade,facade_points,facade_points_rotated_back,angle_facade_rotation,cXorient_facade,h_facade, w_facade, cYorient_facade,auto_complete ,tolerance_x_facade_auto,tolerance_y_facade_auto,y_threshold_facade_auto,n_index_facade_auto)
            else:
                while True:
                    facade_points,facade_points_rotated_back,angle_facade_rotation,cXorient_facade, cYorient_facade,h_facade, w_facade = facade_nodes_detections(grid_cropped,floor,new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2,black_background,auto_complete ,angle_facade_auto)
                    facade_points_df,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade = north_building_facade_pixels_coordinates(floor,letter_horizontal_facade,letter_vertical_facade,facade_points,facade_points_rotated_back,angle_facade_rotation,cXorient_facade, cYorient_facade,h_facade, w_facade,auto_complete,tolerance_x_facade_auto,tolerance_y_facade_auto,y_threshold_facade_auto,n_index_facade_auto)
                    if validate_step(north_building_facade_pixels_coordinates):
                        break
        elif 'HS' in floor: 
            if auto_complete == 'yes':
                facade_points,facade_points_rotated_back,angle_facade_rotation,cXorient_facade, cYorient_facade,h_facade, w_facade = facade_nodes_detections(grid_cropped,floor,new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2,black_background,auto_complete ,angle_facade_auto)
                facade_points_df,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade = south_building_facade_pixels_coordinates(floor,letter_horizontal_facade,letter_vertical_facade,facade_points,facade_points_rotated_back,angle_facade_rotation,cXorient_facade,h_facade, w_facade, cYorient_facade,auto_complete ,tolerance_x_facade_auto,tolerance_y_facade_auto,y_threshold_facade_auto,n_index_facade_auto)
            else:
                while True:
                    facade_points,facade_points_rotated_back,angle_facade_rotation,cXorient_facade, cYorient_facade,h_facade, w_facade = facade_nodes_detections(grid_cropped,floor,new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2,black_background,auto_complete ,angle_facade_auto)
                    facade_points_df,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade = south_building_facade_pixels_coordinates(floor,letter_horizontal_facade,letter_vertical_facade,facade_points,facade_points_rotated_back,angle_facade_rotation,cXorient_facade,h_facade, w_facade, cYorient_facade,auto_complete ,tolerance_x_facade_auto,tolerance_y_facade_auto,y_threshold_facade_auto,n_index_facade_auto)
                    if validate_step(south_building_facade_pixels_coordinates):
                        break
        
        ###
        ###
        ###
        full_df = pixels_matching(auto_complete,floor,floor_points_df,facade_points_df,room_pixels)
        ###
        ###
        ###    
        if auto_complete != 'yes': 
            df = overall_hyperparameters_floors_computer_vision(floor,letter_horizontal,letter_vertical,letter_horizontal_facade,letter_vertical_facade,angle1,angle2,min_size_trapeze_line,x,y,angle_calculation,area_threshold,vertex_threshold,number_false_room,area_threshold_bigger_rooms,bbox_area,aspect_ratio_threshold,balcony_area_detected,number_false_room_transfer,number_balcony_transfer_room,angle_floor_rotation,tolerance_x_floor,tolerance_y_floor,y_threshold_floor,a_index_floor,angle_facade_rotation,tolerance_x_facade,tolerance_y_facade,y_threshold_facade,n_index_facade,kernel_size)