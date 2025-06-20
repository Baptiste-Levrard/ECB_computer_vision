#Importing usual libraries
import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import pandas as pd
import pickle
from tqdm import tqdm
import warnings

#Import projects parameters
from functions.params import ROOT,PLAN_ROOT,PLAN_PNG,VISUALS

#Import helping functions
from functions.pixel_matching_support_functions import *


pd.options.mode.copy_on_write = True
warnings.simplefilter(action='ignore', category=FutureWarning)

def final_df_concatination(floor):
    """
    Add the room variable to the different equipment of the floor. Create an xlsx files in the floor folder composed of all the data realetd to the floor.
    inputs
    floor = str. ex: HN04, HS03...
    output
    writer = xlsx file, composed of the different df as sheets
    """

    coodinates = pd.read_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_pixels_coordinates.csv'))
    if os.path.exists(os.path.join(VISUALS,f'{floor}',f'{floor}_rooms_names_with_wrong_coordinates.csv')):
        wrong_room_name = pd.read_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_rooms_names_with_wrong_coordinates.csv'))
    dict_CV_ECB = pd.read_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_rooms_coordinates_dictionnary.csv'))
    with open(os.path.join(os.getcwd(),VISUALS, f'{floor}', f'{floor}_room_pixels.pkl'),'rb') as f:
        room_pixels = pickle.load(f)
    
    
    coodinates['coordinate_vertical']=coodinates['coordinate_vertical'].apply(lambda x: '{0:0>2}'.format(x))
    coodinates['coordinate_horizontal']=coodinates['coordinate_horizontal'].apply(lambda x: '{0:0>2}'.format(x))
    coodinates['full_coordinates'] = coodinates['letter_horizontal']+coodinates['coordinate_horizontal'].astype(str)+coodinates['letter_vertical']+coodinates['coordinate_vertical'].astype(str)
    
    coodinates['x_axis'] = coodinates['x_axis'].astype(int)
    coodinates['y_axis'] = coodinates['y_axis'].astype(int)
    
    for i,c in tqdm(enumerate(room_pixels),unit='Room',desc="New Coordinates Room Matching",total=len(room_pixels)):
        for index, row in coodinates[coodinates['room'].isnull()].iterrows():
            if check_match_minus_10(row, pd.DataFrame(room_pixels[c], columns=['y_axis', 'x_axis'])):
                coodinates.at[index, 'room'] = f'{c}'
    
    coodinates['room'] = coodinates['room'].astype(float)
    
    # Create a mapping dictionary
    mapping = dict(zip(dict_CV_ECB['Unnamed: 0'], dict_CV_ECB['ecb_names'].drop_duplicates()))
    # Replace values
    coodinates['room'] = coodinates['room'].map(mapping)
    
    condition = coodinates['full_coordinates'].isin(dict_CV_ECB[dict_CV_ECB['one_room_coordinate_supposed'].notna()]['ecb_names'])
    coodinates.loc[condition, 'room'] = coodinates.loc[condition, 'full_coordinates']
    
    equips = pd.read_csv(os.path.join(ROOT,'DATA','ECB-TFM-DATAMngmnt-Equipment-TDM - MPE (1).csv'))
    equips_thing = equips[(equips['AKSfull'].str.contains(f'{floor[:2]}.{floor[-2:]}0'))&(equips['Building']==f'{floor[:2]}')]
    equips_thing['Room']=equips_thing['Axis'].isin(coodinates['full_coordinates'])
    
    mapping = dict(zip(coodinates['full_coordinates'], coodinates['room']))
    
    # Map the values from coordinates['room'] to equips_thing['Axis']
    # If a match is found, use the value from coordinates['room'], otherwise leave it as NaN
    equips_thing['Room'] = equips_thing['Axis'].map(mapping)
    badly_equip_things = equips_thing[~equips_thing['Room'].notna()]
    
    #Number of equipment linked to a wall
    wall_equip_things = badly_equip_things[(badly_equip_things['DIN_276_Beschr.'].str.contains('External walls'))|(badly_equip_things['Axis'].str.contains('00'))]
    
    other_rows = badly_equip_things[~(
            (badly_equip_things['DIN_276_Beschr.'].str.contains('External walls', na=False)) |
            (badly_equip_things['Axis'].str.contains('00', na=False)))]
    if os.path.exists(os.path.join(VISUALS,f'{floor}',f'{floor}_rooms_names_with_wrong_coordinates.csv')):
        with pd.ExcelWriter(os.path.join(VISUALS, f'{floor}', f'{floor}_Full_Infos.xlsx'), engine='openpyxl') as writer:
            # Write the first DataFrame to the first sheet
            coodinates.to_excel(writer, sheet_name=f'Coordinates {floor} ECB', index=False)
            dict_CV_ECB.to_excel(writer, sheet_name='Rooms Dictionnary', index=False)
            wrong_room_name.to_excel(writer, sheet_name='Wrong Rooms Name', index=False)
            equips_thing[equips_thing['Room'].notna()].to_excel(writer, sheet_name=f'Equipment {floor}', index=False)
            other_rows.to_excel(writer, sheet_name='Wrong Equipment Position', index=False)
            wall_equip_things.to_excel(writer, sheet_name='Wall Equipment', index=False)
            writer.close()
    else:
        with pd.ExcelWriter(os.path.join(VISUALS, f'{floor}', f'{floor}_Full_Infos.xlsx'), engine='openpyxl') as writer:
            # Write the first DataFrame to the first sheet
            coodinates.to_excel(writer, sheet_name=f'Coordinates {floor} ECB', index=False)
            dict_CV_ECB.to_excel(writer, sheet_name='Rooms Dictionnary', index=False)
            equips_thing[equips_thing['Room'].notna()].to_excel(writer, sheet_name=f'Equipment {floor}', index=False)
            other_rows.to_excel(writer, sheet_name='Wrong Equipment Position', index=False)
            wall_equip_things.to_excel(writer, sheet_name='Wall Equipment', index=False)
            writer.close()

    return writer