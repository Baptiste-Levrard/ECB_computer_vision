import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

import cv2
import numpy as np
import pandas as pd

def top_room_detection(floor,rooms,full_coordinates_pixels,CV_room_coordinates_top_left,auto_complete,big_room_variable_auto):
    """
    Input
    floor=str. The floor used for the script. Must be spelled HN05 or HS04...
    rooms= DF. Preprocessed ECB rooms names
    full_coordinates_pixels: DF 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. Full DF of the coordinates of the floor
    CV_room_coordinates_top_left: dict. two columns - One for the index, the other one for the Coordinate
        
    Output
    big_room_variable= int. Number of room that align in size for ECB and CV method
    FINAL_DF_CV_room_coordinates_top_left: DF. 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. DF of the CV detected rooms and there TOP left coordinates and pixels position.
    big_size_rooms_and_pixels_coordinates:  DF. 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. DF of the size align rooms between ECB and CV method
    """
    #Room Detection
    DF_CV_room_coordinates_top_left = pd.DataFrame.from_dict(CV_room_coordinates_top_left, orient='index', columns=['coordinates_ECB_space'])
    DF_CV_room_coordinates_top_left = DF_CV_room_coordinates_top_left.reset_index()
    FINAL_DF_CV_room_coordinates_top_left = pd.merge(DF_CV_room_coordinates_top_left, full_coordinates_pixels,how="inner",on=["coordinates_ECB_space", "coordinates_ECB_space"])
    if auto_complete == 'yes':
        big_room_variable = int(big_room_variable_auto)
    else:
        while True:
            try:
                big_room_variable=int(input(f"Numbers of rooms that are identical by size in both he CV and the ECB architectural measuring. int() ex: 4.").strip().lower())
                break
            except ValueError:
                print("Invalid input.")
    
    #Creating the DataFrame for the big rooms
    size_rooms_accurate = rooms[:big_room_variable]
    big_size_rooms_and_pixels_coordinates = pd.merge(full_coordinates_pixels,size_rooms_accurate,how="inner",on=["coordinates_ECB_space", "coordinates_ECB_space"])
    big_size_rooms_and_pixels_coordinates = big_size_rooms_and_pixels_coordinates.sort_values(['SP_Dimension Net'],ascending=False)
    
    #Doing the same for the Computer Vision detected
    FINAL_DF_CV_room_coordinates_top_left_top_10 = FINAL_DF_CV_room_coordinates_top_left.sort_values(['room'])[:big_room_variable]
    
    #Enables to make changes using an iteration on the big_room value and choose the 
    image = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}', f'{floor}_Blacked.png'))
    image2 = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}', f'{floor}_Blacked.png'))
    for index, row in big_size_rooms_and_pixels_coordinates.reset_index().iterrows():
        cv2.circle(image, (int(row['x_axis']),int(row['y_axis'])), radius=0, color=(0, 0, 255), thickness=3)
        cv2.rectangle(image, ((int(row['x_axis']),int(row['y_axis'])+10)),((int(row['x_axis'])+110),int(row['y_axis'])-10), color=(255, 255, 0), thickness =-1)
        cv2.putText(image, (str(index)+'.  '+str(row['letter_horizontal'])+str(row['coordinate_horizontal'])+str(row['letter_vertical'])+str(row['coordinate_vertical'])), (int(row['x_axis']),int(row['y_axis'])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 150, 0), 2)
    image = cv2.resize(image, (0,0), fx=0.80, fy=0.80)
    
    for index, row in FINAL_DF_CV_room_coordinates_top_left_top_10.reset_index().iterrows():
        cv2.circle(image2, (int(row['x_axis']),int(row['y_axis'])), radius=0, color=(0, 0, 255), thickness=3)
        cv2.rectangle(image2, ((int(row['x_axis']),int(row['y_axis'])+10)),((int(row['x_axis'])+110),int(row['y_axis'])-10), color=(255, 255, 0), thickness =-1)
        cv2.putText(image2, (str(index)+'.  '+str(row['letter_horizontal'])+str(row['coordinate_horizontal'])+str(row['letter_vertical'])+str(row['coordinate_vertical'])), (int(row['x_axis']),int(row['y_axis'])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 150, 0), 2)
    image2 = cv2.resize(image2, (0,0), fx=0.80, fy=0.80)
    
    numpy_horizontal_concat = np.concatenate((image, image2), axis=0) #0:Vertical
    

    if not auto_complete == 'yes':
        cv2.imshow(f'Comparison big rooms positions -- {floor} | Top ECB | Bottom CV', numpy_horizontal_concat)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('top_room_detection -Status: Done')
    return big_room_variable,FINAL_DF_CV_room_coordinates_top_left,big_size_rooms_and_pixels_coordinates