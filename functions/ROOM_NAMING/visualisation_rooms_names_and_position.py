import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

import cv2
import numpy as np

def visualisation_rooms_names_and_position(floor,auto_complete,big_size_rooms_and_pixels_coordinates,FINAL_DF_room_and_inside_pixels_coordinates,FINAL_DF_distance_coordinates_list_one_coordinates,not_assigned_rooms_and_pixels_coordinates,FINAL_DF_CV_room_coordinates_top_left):
    """
    Script that would build to images of the floor. On top the floor with the ECB coordinates. At the bottom the floor with the CV deducted coordinates.
    Save it under the floor folder.

    input

    floor: str. Floor's name e.g. HS04
    big_size_rooms_and_pixels_coordinates: df with ['x_axis'], ['y_axis'], ['letter_horizontal'], ['coordinate_horizontal'], ['letter_vertical'], ['coordinate_vertical']  columns. 
    FINAL_DF_room_and_inside_pixels_coordinates: df with ['x_axis'], ['y_axis'], ['letter_horizontal'], ['coordinate_horizontal'], ['letter_vertical'], ['coordinate_vertical']  columns. 
    FINAL_DF_distance_coordinates_list_one_coordinates: df with ['x_axis'], ['y_axis'], ['letter_horizontal'], ['coordinate_horizontal'], ['letter_vertical'], ['coordinate_vertical']  columns.
    not_assigned_rooms_and_pixels_coordinates: df with ['x_axis'], ['y_axis'], ['letter_horizontal'], ['coordinate_horizontal'], ['letter_vertical'], ['coordinate_vertical']  columns.
    FINAL_DF_baptiste_room_coordinates_top_left: df with ['x_axis'], ['y_axis'], ['letter_horizontal'], ['coordinate_horizontal'], ['letter_vertical'], ['coordinate_vertical']  columns.

    return 'Comparison floor -- {floor}, ECB Coordinates up, Computer Vision attributed coordinates down.png' in floor folder.
    
    
    """
    #plot the pixels coordinates of the different iterations
    image = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}', f'{floor}_Blacked.png'))
    height, width, _ = image.shape  # Get image dimensions (height, width, channels)
    for index, row in big_size_rooms_and_pixels_coordinates.iterrows():
        cv2.circle(image, (int(row['x_axis']),int(row['y_axis'])), radius=0, color=(0, 0, 255), thickness=3)
        cv2.rectangle(image, ((int(row['x_axis']),int(row['y_axis'])+3)),((int(row['x_axis'])+28),int(row['y_axis'])-8), color=(255, 255, 0), thickness =-1)
        cv2.putText(image, (str(row['letter_horizontal'])+str(row['coordinate_horizontal'])+str(row['letter_vertical'])+str(row['coordinate_vertical'])), (int(row['x_axis']),int(row['y_axis'])), cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 150, 0), 1)
    for index, row in FINAL_DF_room_and_inside_pixels_coordinates.iterrows():
        cv2.circle(image, (int(row['x_axis']),int(row['y_axis'])), radius=0, color=(0, 0, 255), thickness=3)
        cv2.rectangle(image, ((int(row['x_axis']),int(row['y_axis'])+3)),((int(row['x_axis'])+28),int(row['y_axis'])-8), color=(255, 0, 255), thickness =-1)
        cv2.putText(image, (str(row['letter_horizontal'])+str(row['coordinate_horizontal'])+str(row['letter_vertical'])+str(row['coordinate_vertical'])), (int(row['x_axis']),int(row['y_axis'])), cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 150, 0), 1)
    for index, row in FINAL_DF_distance_coordinates_list_one_coordinates.iterrows():
        cv2.circle(image, (int(row['x_axis']),int(row['y_axis'])), radius=0, color=(0, 0, 255), thickness=3)
        cv2.rectangle(image, ((int(row['x_axis']),int(row['y_axis'])+3)),((int(row['x_axis'])+28),int(row['y_axis'])-8), color=(0, 255, 255), thickness =-1)
        cv2.putText(image, (str(row['letter_horizontal'])+str(row['coordinate_horizontal'])+str(row['letter_vertical'])+str(row['coordinate_vertical'])), (int(row['x_axis']),int(row['y_axis'])), cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 150, 0), 1)
    for index, row in not_assigned_rooms_and_pixels_coordinates.iterrows():
        cv2.circle(image, (int(row['x_axis']),int(row['y_axis'])), radius=0, color=(0, 0, 255), thickness=3)
        cv2.rectangle(image, ((int(row['x_axis']),int(row['y_axis'])+3)),((int(row['x_axis'])+28),int(row['y_axis'])-8), color=(210, 210, 210), thickness =-1)
        cv2.putText(image, (str(row['letter_horizontal'])+str(row['coordinate_horizontal'])+str(row['letter_vertical'])+str(row['coordinate_vertical'])), (int(row['x_axis']),int(row['y_axis'])), cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 150, 0), 1)
    
    #Legend
    cv2.putText(image, ('Legend: How did the rooms got attributed'), (50,height-110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.rectangle(image, (20,height-90), (30,height-80), color=(255, 255, 0), thickness =-1)
    cv2.putText(image, ('Teal - TOP 10 rooms by size '), (50,height-80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.rectangle(image, (20,height-70), (30,height-60), color=(255, 0, 255), thickness =-1)
    cv2.putText(image, ('Magenta - Coordinates detected in room area'), (50,height-60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
    cv2.rectangle(image, (20,height-50), (30,height-40), color=(0, 255, 255), thickness =-1)
    cv2.putText(image, ('Yellow - Coordinates attributed to closest pixels neighbour'), (50,height-40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    cv2.rectangle(image, (20,height-30), (30,height-20), color=(210, 210, 210), thickness =-1)
    cv2.putText(image, ('Grey - Rooms not found by using CV'), (50,height-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (210, 210, 210), 1)
    #Resize by half
    image = cv2.resize(image, (0,0), fx=0.80, fy=0.80)
    
    
    #Repeat the process
    #plot the pixels coordinates of the computer vision attributed coordinates
    image2 = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}', f'{floor}_Blacked.png'))
    for index, row in FINAL_DF_CV_room_coordinates_top_left.iterrows():
        cv2.circle(image2, (int(row['x_axis']),int(row['y_axis'])), radius=0, color=(0, 0, 255), thickness=3)
        cv2.rectangle(image2, ((int(row['x_axis']),int(row['y_axis'])+3)),((int(row['x_axis'])+28),int(row['y_axis'])-8), color=(255, 255, 255), thickness =-1)
        cv2.putText(image2, (str(row['letter_horizontal'])+str(row['coordinate_horizontal'])+str(row['letter_vertical'])+str(row['coordinate_vertical'])), (int(row['x_axis']),int(row['y_axis'])), cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 150, 0), 1)
    #Legend
    cv2.putText(image2, ('Legend:'), (50,height-50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.rectangle(image2, (20,height-30), (30,height-20), color=(255, 255, 255), thickness =-1)
    cv2.putText(image2, ('White - Top left coordinate of the room - using CV'), (50,height-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    image2 = cv2.resize(image2, (0,0), fx=0.80, fy=0.80)
    
    #CV2 being arrays of pixels - Numpy concepts can be used
    numpy_horizontal_concat = np.concatenate((image, image2), axis=0) #0:Vertical
    
    if not auto_complete == 'yes':
        cv2.imshow(f'Comparison floor -- {floor} | ECB Coordinates up | Computer Vision attributed coordinates down', numpy_horizontal_concat)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('visualisation_rooms_names_and_position -Status: Done')
        
    return cv2.imwrite(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'Comparison floor -- {floor}, ECB Coordinates up, Computer Vision attributed coordinates down.png'),numpy_horizontal_concat)