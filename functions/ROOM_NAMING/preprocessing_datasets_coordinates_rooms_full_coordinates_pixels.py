import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

import numpy as np
import pandas as pd

def preprocessing_datasets_coordinates_rooms_full_coordinates_pixels(floor,rooms):
    """
    Using the dataset collected using Computer Vision (CV) and Architectural data (SQM2, room coordinates) preprocess the data to be then compared and attributed to the same room coordinates.
    
    Input
    floor=str. The floor used for the script. Must be spelled HN05 or HS04...
    rooms= DF. Preprocessed ECB rooms names

    Output
    full_coordinates_pixels: DF 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. Full DF of the coordinates of the floor
    CV_room_coordinates_top_left: dict. two columns - One for the index, the other one for the Coordinate
    floor_room_pixels_coordinates : DF 3 main columns [x_axis],[y_axis],[coordinates_ECB_space]. DF of the coordinates extarcted of the ECB's rooms name.
    """
    ##Formatting CV datasets
    ##
    ##
    ##
    ##

    floor_room_pixels_coordinates = pd.read_csv(os.path.join(VISUALS, f'{floor}', f'{floor}_pixels_coordinates.csv'))
    floor_room_pixels_coordinates['sum']=floor_room_pixels_coordinates['coordinate_horizontal']+floor_room_pixels_coordinates['coordinate_vertical']
    floor_room_pixels_coordinates_without_nan = floor_room_pixels_coordinates.dropna(subset=['room'])
    
    #Change the column to a str type, and if the lenght of the str is not of exactly 2, add a zero infront
    floor_room_pixels_coordinates['coordinate_horizontal'] = floor_room_pixels_coordinates['coordinate_horizontal'].astype(str).str.zfill(2)
    floor_room_pixels_coordinates['coordinate_vertical'] = floor_room_pixels_coordinates['coordinate_vertical'].astype(str).str.zfill(2)
    #Associate the all the columns into one that correspond to the room coordinates format of the ECB
    #Render the previous cell obsolete - Think about modifying it.
    floor_room_pixels_coordinates['coordinates_ECB_space']=floor_room_pixels_coordinates['letter_horizontal']+floor_room_pixels_coordinates['coordinate_horizontal']+floor_room_pixels_coordinates['letter_vertical']+floor_room_pixels_coordinates['coordinate_vertical']
    
    CV_room_coordinates_top_left={}
    for i in floor_room_pixels_coordinates_without_nan['room'].unique():
        if floor_room_pixels_coordinates[floor_room_pixels_coordinates['room']==i]['letter_vertical'].nunique() == 1:
            xx = floor_room_pixels_coordinates[(floor_room_pixels_coordinates['room']==i)]
            xxx = xx[xx['coordinate_horizontal']==min(xx['coordinate_horizontal'])]
            CV_room_coordinates_top_left[i] = xxx[xxx['coordinate_vertical']==min(xxx['coordinate_vertical'])]['coordinates_ECB_space'].iloc[0]
        else:
            if 'HS' in floor:
                xx = floor_room_pixels_coordinates[(floor_room_pixels_coordinates['room']==i)&(floor_room_pixels_coordinates['letter_horizontal']=='A')]
                xxx = xx[xx['coordinate_horizontal']==min(xx['coordinate_horizontal'])]
                CV_room_coordinates_top_left[i] = xxx[xxx['coordinate_vertical']==min(xxx['coordinate_vertical'])]['coordinates_ECB_space'].iloc[0]
            else:
                xx = floor_room_pixels_coordinates[(floor_room_pixels_coordinates['room']==i)&(floor_room_pixels_coordinates['letter_horizontal']=='N')]
                xxx = xx[xx['coordinate_horizontal']==min(xx['coordinate_horizontal'])]
                CV_room_coordinates_top_left[i] = xxx[xxx['coordinate_vertical']==min(xxx['coordinate_vertical'])]['coordinates_ECB_space'].iloc[0]
    
    
    #Full coordinates and pixels coordinates
    #Second is useful for Distance calculation between two points
    ##
    ##
    ##
    ##
    
    full_coordinates_pixels = pd.read_csv(os.path.join(os.getcwd(),VISUALS, f'{floor}', f'{floor}_pixels_coordinates.csv'))
    full_coordinates_pixels['coordinate_vertical']=full_coordinates_pixels['coordinate_vertical'].apply(lambda x: '{0:0>2}'.format(x))
    full_coordinates_pixels['coordinate_horizontal']=full_coordinates_pixels['coordinate_horizontal'].apply(lambda x: '{0:0>2}'.format(x))
    full_coordinates_pixels['coordinates_ECB_space'] = full_coordinates_pixels['letter_horizontal']+full_coordinates_pixels['coordinate_horizontal']+full_coordinates_pixels['letter_vertical']+full_coordinates_pixels['coordinate_vertical']
    
    dictionnary_letters = {}
    for i in floor_room_pixels_coordinates['letter_horizontal'].unique():
        j = floor_room_pixels_coordinates[floor_room_pixels_coordinates['letter_horizontal']==i]['letter_vertical'].loc[floor_room_pixels_coordinates[floor_room_pixels_coordinates['letter_horizontal']==i]['letter_vertical'].idxmax()]
        dictionnary_letters[i] = j
    
    rooms_names_with_wrong_coordinates = pd.DataFrame()
    #Add the coordinates of the rooms that to the pixel data set - should it be or not ; Improvement point.
    df1 = pd.read_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_pixels_coordinates.csv'))
    for i in rooms['coordinates_ECB_space']:
        letter_horizontal = i[0]
        coordinate_horizontal = i[1:3]
        coordinate_horizontal=np.int64(coordinate_horizontal)
        letter_vertical = i[3]
        coordinate_vertical = i[4:6]
        coordinate_vertical=np.int64(coordinate_vertical)
        if dictionnary_letters.get(letter_horizontal) != letter_vertical or dictionnary_letters.get(letter_horizontal) is None:
            rooms_names_with_wrong_coordinates = pd.concat([rooms_names_with_wrong_coordinates,rooms[rooms['coordinates_ECB_space']==i]])
        else:
            if i not in floor_room_pixels_coordinates['coordinates_ECB_space'].values:
                identical_horizontal_coordinates=df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_vertical']==coordinate_vertical)].drop(columns=['letter_horizontal','letter_vertical']).groupby(['coordinate_horizontal']).mean().sort_values(['coordinate_horizontal']).reset_index()
                identical_horizontal_coordinates['other']=identical_horizontal_coordinates['x_axis'].diff()
                coordinate_horizontal_diff = identical_horizontal_coordinates['coordinate_horizontal'].diff()
                mean_vertical_coordinates = identical_horizontal_coordinates[coordinate_horizontal_diff == 1]['other'].mean()
                identical_vertical_coordinates=df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_vertical']==coordinate_vertical)].drop(columns=['letter_horizontal','letter_vertical']).groupby(['coordinate_horizontal']).mean().sort_values(['coordinate_horizontal']).reset_index()
                identical_vertical_coordinates['other']=identical_vertical_coordinates['x_axis'].diff()
                coordinate_vertical_diff = identical_vertical_coordinates['coordinate_horizontal'].diff()
                mean_horizontal_coordinates = identical_vertical_coordinates[coordinate_vertical_diff == 1]['other'].mean()
        
                
                if not np.isnan(df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical-1)]['x_axis'].mean()):#+mean_vertical_coordinates):
                    x_axis=df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical-1)]['x_axis'].mean()#+mean_vertical_coordinates
                #Check if it is the first value on the axis x. If it is the case, will select the x_axis value of the next horizontal coordinate + the vertical 01 - An arbitrary choice but from the entierty of the project - There is always a coordinat 01 and subtract the means
                elif not np.isnan(df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical+1)]['x_axis'].mean()):#-mean_vertical_coordinates):
                    x_axis=df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical+1)]['x_axis'].mean()#-mean_vertical_coordinates
                # From here in the localisation, I brain farted. 
                elif not np.isnan(df1[(df1['letter_vertical']==letter_vertical)&(df1['coordinate_vertical']==coordinate_vertical)&(df1['coordinate_horizontal']==coordinate_horizontal+1)]['x_axis'].mean()-mean_vertical_coordinates):
                    x_axis=df1[(df1['letter_vertical']==letter_vertical)&(df1['coordinate_vertical']==coordinate_vertical)&(df1['coordinate_horizontal']==coordinate_horizontal+1)]['x_axis'].mean()-mean_vertical_coordinates
                elif not np.isnan(df1[(df1['letter_vertical']==letter_vertical)&(df1['coordinate_vertical']==coordinate_vertical)&(df1['coordinate_horizontal']==coordinate_horizontal-1)]['x_axis'].mean()+mean_vertical_coordinates):
                    x_axis=df1[(df1['letter_vertical']==letter_vertical)&(df1['coordinate_vertical']==coordinate_vertical)&(df1['coordinate_horizontal']==coordinate_horizontal-1)]['x_axis'].mean()+mean_vertical_coordinates
                if np.isnan(x_axis):
                    #print(f'Issue at {floor} -- {letter_horizontal}{coordinate_horizontal}{letter_vertical}{coordinate_vertical}')
                    coordinate_horizontal='{0:0>2}'.format(coordinate_horizontal)
                    coordinate_vertical='{0:0>2}'.format(coordinate_vertical)
                    test_equipment = df2[df2['Axis'].isin([f'{letter_horizontal}{coordinate_horizontal}{letter_vertical}{coordinate_vertical}'])]
                    test = pd.concat([test, test_equipment], ignore_index=True)
                    continue
                    
                #####Same process for Y axis
                
                #Check if it is the first value on the axis y. If it is the case, will select the x_axis value of the next vertical coordinate + the maximal horizontal coordinate -1 - An arbitrary choice but from the entierty of the project - seems like it is representated everytime - See how it scales for GW and subtract the means
                if not np.isnan(df1[(df1['letter_vertical']==letter_vertical)&(df1['coordinate_vertical']==coordinate_vertical)&(df1['coordinate_horizontal']==coordinate_horizontal-1)]['y_axis'].mean()):#-mean_horizontal_coordinates):
                    y_axis=df1[(df1['letter_vertical']==letter_vertical)&(df1['coordinate_vertical']==coordinate_vertical)&(df1['coordinate_horizontal']==coordinate_horizontal-1)]['y_axis'].mean()#-mean_horizontal_coordinates
                #Check if it is the first value on the axis x. If it is the case, will select the x_axis value of the next horizontal coordinate + the vertical 01 - An arbitrary choice but from the entierty of the project - There is always a coordinat 01 and subtract the means
                elif not np.isnan(df1[(df1['letter_vertical']==letter_vertical)&(df1['coordinate_vertical']==coordinate_vertical)&(df1['coordinate_horizontal']==coordinate_horizontal+1)]['y_axis'].mean()):#+mean_horizontal_coordinates):
                    y_axis=df1[(df1['letter_vertical']==letter_vertical)&(df1['coordinate_vertical']==coordinate_vertical)&(df1['coordinate_horizontal']==coordinate_horizontal+1)]['y_axis'].mean()#+mean_horizontal_coordinates
                # From here, I branfarted
                if not (letter_vertical=='Q' or letter_vertical=='M'):
                    if not np.isnan(df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical-1)]['y_axis'].mean()-mean_horizontal_coordinates):
                        y_axis=df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical-1)]['y_axis'].mean()-mean_horizontal_coordinates
                    elif not np.isnan(df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical+1)]['y_axis'].mean()+mean_horizontal_coordinates):
                        y_axis=df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical+1)]['y_axis'].mean()+mean_horizontal_coordinates
                else:
                    if not np.isnan(df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical-1)]['y_axis'].mean()+mean_horizontal_coordinates):
                        y_axis=df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical-1)]['y_axis'].mean()+mean_horizontal_coordinates
                    elif not np.isnan(df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical+1)]['y_axis'].mean()-mean_horizontal_coordinates):
                        y_axis=df1[(df1['letter_horizontal']==letter_horizontal)&(df1['coordinate_horizontal']==coordinate_horizontal)&(df1['coordinate_vertical']==coordinate_vertical+1)]['y_axis'].mean()-mean_horizontal_coordinates
                    
                if np.isnan(y_axis):                
                    #print(f'Issue at {floor} -- {letter_horizontal}{coordinate_horizontal}{letter_vertical}{coordinate_vertical}')
                    coordinate_horizontal='{0:0>2}'.format(coordinate_horizontal)
                    coordinate_vertical='{0:0>2}'.format(coordinate_vertical)
                    test_equipment = df2[df2['Axis'].isin([f'{letter_horizontal}{coordinate_horizontal}{letter_vertical}{coordinate_vertical}'])]
                    test = pd.concat([test, test_equipment], ignore_index=True)
                    continue
                
                temp = pd.DataFrame({
                    'letter_horizontal':letter_horizontal,
                    'coordinate_horizontal':coordinate_horizontal,
                    'x_axis':round(x_axis),
                    'letter_vertical':letter_vertical,
                    'coordinate_vertical':coordinate_vertical,
                    'y_axis':round(y_axis),
                    'coordinates_ECB_space':i[0]+i[1:3]+i[3]+i[4:6]},index=[0])
                full_coordinates_pixels = pd.concat([full_coordinates_pixels, temp], ignore_index=True)

    if not rooms_names_with_wrong_coordinates.empty:
        rooms_names_with_wrong_coordinates.to_csv(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_rooms_names_with_wrong_coordinates.csv'), index=False)

    print('preprocessing_datasets_coordinates_rooms_full_coordinates_pixels -Status: Done')
        
    return full_coordinates_pixels,CV_room_coordinates_top_left,floor_room_pixels_coordinates