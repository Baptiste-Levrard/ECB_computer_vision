import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import cv2
import pandas as pd
import csv
from tqdm import tqdm

from functions.params import ROOT,PLAN_ROOT,VISUALS,PLAN_PNG
from functions.pixel_matching_support_functions import *

def pixels_matching(auto_complete,floor,floor_points_df,facade_points_df,room_pixels):
    """Match pixels positions of the rooms to the labels coordinates.
    floor_points_df=df. Require ['y_axis_calculation'] and ['x_axis_calculation']
    facade_points_df=df. Require ['y_axis_calculation'] and ['x_axis_calculation']
    return
    full_df=df. Pixels position of coordinates for both facade and floor position.
    """
    full_df = pd.concat([floor_points_df, facade_points_df], ignore_index=True)

    # Iterate over df1 and update the 'matched' column
    for i,c in tqdm(enumerate(room_pixels),unit='Room',desc="1/5 round coordinates iteration",total=len(room_pixels)):
        for index, row in full_df.iterrows():
            if check_match(row, pd.DataFrame(room_pixels[c], columns=['y_axis', 'x_axis'])):
                full_df.at[index, 'room'] = f'{c}'
    
    for i,c in tqdm(enumerate(room_pixels),unit='Room',desc="2/5 round coordinates iteration",total=len(room_pixels)):
        for index, row in full_df[full_df['room'].isnull()].iterrows():
            if check_match_plus_5(row, pd.DataFrame(room_pixels[c], columns=['y_axis', 'x_axis'])):
                full_df.at[index, 'room'] = f'{c}'
    
    for i,c in tqdm(enumerate(room_pixels),unit='Room',desc="3/5 round coordinates iteration",total=len(room_pixels)):
        for index, row in full_df[full_df['room'].isnull()].iterrows():
            if check_match_plus_15_horizontal_axis(row, pd.DataFrame(room_pixels[c], columns=['y_axis', 'x_axis'])):
                full_df.at[index, 'room'] = f'{c}'
    
    for i,c in tqdm(enumerate(room_pixels),unit='Room',desc="4/5 round coordinates iteration",total=len(room_pixels)):
        for index, row in full_df[full_df['room'].isnull()].iterrows():
            if check_match_plus_15_vertical_axis(row, pd.DataFrame(room_pixels[c], columns=['y_axis', 'x_axis'])):
                full_df.at[index, 'room'] = f'{c}'
    
    for i,c in tqdm(enumerate(room_pixels),unit='Room',desc="5/5 round coordinates iteration",total=len(room_pixels)):
        for index, row in full_df[full_df['room'].isnull()].iterrows():
            if check_match_minus_10(row, pd.DataFrame(room_pixels[c], columns=['y_axis', 'x_axis'])):
                full_df.at[index, 'room'] = f'{c}'

    image = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_Blacked.png'))
    for index, row in full_df[full_df['room'].isnull()].iterrows():
        cv2.circle(image, (row['x_axis'],row['y_axis']), radius=0, color=(0, 0, 255), thickness=3)
        cv2.rectangle(image, ((row['x_axis'],row['y_axis']+3)),((row['x_axis']+28),(row['y_axis']-8)), color=(255, 255, 255), thickness =-1)
        cv2.putText(image, (str(row['letter_horizontal'])+str(row['coordinate_horizontal'])+str(row['letter_vertical'])+str(row['coordinate_vertical'])), (row['x_axis'],row['y_axis']), cv2.FONT_HERSHEY_PLAIN, 0.5, (255, 150, 0), 1)
    if not auto_complete == 'yes':
        cv2.imshow('Unmatched coordinates', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print('pixels_matching -Status: Done')
    cv2.imwrite(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_MISSING_COORDINATES.png'),image)
    full_df.to_csv(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_pixels_coordinates.csv'),index=False)
    
    return full_df