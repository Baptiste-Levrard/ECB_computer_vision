import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd
import numpy as np
import csv
import cv2
from tqdm import tqdm

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

def coordinates_mathematical_finding():
    '''
    The function unlike the previous part of the project has been scripted with a full view of datasets in mind. 
    No requirements for variables necessary as every thing has been handled during previous part of the project.
    
    For each floors preprocessed, we retrieve the missing coordinates of the equipment that havent been matched. 
    
    return DF_MAIN: pandas df. 
    '''
    pd.options.mode.copy_on_write = True
    
    test = pd.DataFrame(columns=['AKSfull','Building','Level','Axis','Roomzone','AKSGS1','AKS_GS2','AKS_GS3','AKS_GS4','Description','Manufacturer','Model_Version','Serial_number','Supplier.Name','DIN_276_Code','DIN_276_Beschr.','Code','K3-Code','Status.Label','FuncLoc-Code','MainEquipmentAKS ull','isin_method'])
    DF_MAIN = pd.read_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'))
    
    for index, row in tqdm(enumerate(DF_MAIN.iterrows()),unit='Floor',total=len(DF_MAIN)):
        floor = row[1]['floor']
        df1 = pd.read_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_pixels_coordinates.csv'))
        df2 = pd.read_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_equipment_mismatched_baptiste_changes.csv'))
        df1['coordinate_horizontal']=df1['coordinate_horizontal'].astype(int)
        df1['coordinate_vertical']=df1['coordinate_vertical'].astype(int)
        for l in range(len(df2['Axis'].unique())):
            
            letter_horizontal=df2['Axis'].unique()[l][0]
            coordinate_horizontal=df2['Axis'].unique()[l][1:3]
            coordinate_horizontal=np.int64(coordinate_horizontal)
            letter_vertical=df2['Axis'].unique()[l][3]
            coordinate_vertical=df2['Axis'].unique()[l][4:6]
            coordinate_vertical=np.int64(coordinate_vertical)
            x_axis = np.nan
            y_axis = np.nan
            
            #Check if there is a mathematical outcome to the equation, if yes, select it for the new x_axis value
            #Lenghty but easy formula; Looking for the two values on the same X_ axiso	
            #Select only the two previous coordinates (EX: A25L6 – A25L7 to calculate A25. And A24L8 – A23L8 to calculate L8)
    
            
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
                'x_axis':x_axis,
                'letter_vertical':letter_vertical,
                'coordinate_vertical':coordinate_vertical,
                'y_axis':y_axis},index=[0])
    
            
            df1 = pd.concat([df1, temp], ignore_index=True)
            df1.to_csv(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_pixels_coordinates.csv'), index=False)
                
    
        test.to_csv(os.path.join(os.getcwd(),VISUALS,'equipments_to_be_moved_test.csv'), index=False)
        image = cv2.imread(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_Grid.png'))
        pixel_coordinates = pd.read_csv(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_pixels_coordinates.csv'))
        for s, f in df1.iterrows():
            x=f['x_axis']
            y=f['y_axis']
            letter_horizontal=f['letter_horizontal']
            coordinate_horizontal=f['coordinate_horizontal']
            letter_vertical=f['letter_vertical']
            coordinate_vertical=f['coordinate_vertical']
            label = f"{letter_horizontal}{coordinate_horizontal}{letter_vertical}{coordinate_vertical}"
            position = (int(x), int(y))
            cv2.putText(image, label, position, cv2.FONT_HERSHEY_PLAIN, 0.5, (100, 100, 100), 1)
        cv2.imwrite(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_Grid_Labels_Missing_coordinates_calculated_final_try.png'),image)
        #cv2.imshow(f'Image {floor} with Custom Labels', image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    print('Second round of coordinates matching vs equipment done.')
    return DF_MAIN