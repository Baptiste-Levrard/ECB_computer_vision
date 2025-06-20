import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd
import numpy as np
import csv
from tqdm import tqdm



from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

def rooms_coordinates_equipment_coordinates_matching():
    '''
    The function unlike the previous part of the project has been scripted with a full view of datasets in mind. 
    No requirements for variables necessary as every thing has been handled during previous part of the project.
    
    For each floors preprocessed, the equipments are retrieved from the Planon Dataset (not real time nor close to real time.) previously downloaded.
    This Datset is stored in Data folder under the name : ECB-TFM-DATAMngmnt-Equipment-TDM - MPE (1).csv.
    Must have columns: AKSfull, Axis, DIN_276_Beschr.
    Some requirements have been hardcoded as are paramerters that often pop up in the analysis of the equipment.
    Return for each floor a list with full information of the equipment based on ;
    _equipment_total_unmatched
    _equipment_wall
    _equipment_not_well_associated_CRE
    _equipment_mismatched_baptiste_changes
    
    And create as well in Visual, the number equipment in each category - for every floor
    
    return DF_MAIN: pandas df. 
    '''
    pd.options.mode.copy_on_write = True
    
    equips = pd.read_csv(os.path.join(ROOT,'DATA','ECB-TFM-DATAMngmnt-Equipment-TDM - MPE (1).csv'))
    
    equips = equips[equips['AKSfull'].notna()]
    DF_MAIN = pd.read_csv(os.path.join(VISUALS,'overall_hyperparameters_floors_computer_vision.csv'))
    
    for index, row in tqdm(enumerate(DF_MAIN.iterrows()),unit='Floor',total=len(DF_MAIN)):
    # Extract values from specific columns
        floor = row[1]['floor']
        letter_horizontal = row[1]['letter_horizontal']
        letter_vertical = row[1]['letter_vertical']
        letter_horizontal_facade = row[1]['letter_horizontal_facade']
        letter_vertical_facade = row[1]['letter_vertical_facade']
        coodinates = pd.read_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_pixels_coordinates.csv'))
        coodinates['coordinate_vertical']=coodinates['coordinate_vertical'].apply(lambda x: '{0:0>2}'.format(x))
        coodinates['coordinate_horizontal']=coodinates['coordinate_horizontal'].apply(lambda x: '{0:0>2}'.format(x))
        coodinates['full_coordinates'] = coodinates['letter_horizontal']+coodinates['coordinate_horizontal'].astype(str)+coodinates['letter_vertical']+coodinates['coordinate_vertical'].astype(str)
        equips_thing = equips[(equips['AKSfull'].str.contains(f'{floor[:2]}.{floor[-2:]}0'))&(equips['Building']==f'{floor[:2]}')]
        equips_thing['isin_method']=equips_thing['Axis'].isin(coodinates['full_coordinates'])
    
        
        #Number of UnMatched Equipments
        try_hard_fool = equips_thing[equips_thing['isin_method']==False]
        try_hard_fool.to_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_equipment_total_unmatched.csv'), index=False)
        df1 = equips_thing[equips_thing['isin_method']==False]
    
        
        #Number of equipment linked to a wall
        the_mother_ship = equips_thing[(equips_thing['DIN_276_Beschr.'].str.contains('External walls'))|(equips_thing['Axis'].str.contains('00'))]
        the_mother_ship.to_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_equipment_wall.csv'), index=False)
    
        
        #Number of equipment not well associated
        hey_joe = equips_thing[~(equips_thing['Axis'].str[0].isin([f'{letter_horizontal}']) & (equips_thing['Axis'].str[3].isin([f'{letter_vertical}'])) | equips_thing['Axis'].str[0].isin([f'{letter_horizontal_facade}']) & (equips_thing['Axis'].str[3].isin([f'{letter_vertical_facade}'])))]
        souffle_le_vent = equips_thing[equips_thing['Axis'].isin(['A58L02','A55L04'])]
        hey_joe = pd.concat([hey_joe,souffle_le_vent],ignore_index=True)
        hey_joe.to_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_equipment_not_well_associated_CRE.csv'), index=False)
        
        df2 = equips_thing[~(equips_thing['Axis'].str[0].isin([f'{letter_horizontal}']) & (equips_thing['Axis'].str[3].isin([f'{letter_vertical}'])) | equips_thing['Axis'].str[0].isin([f'{letter_horizontal_facade}']) & (equips_thing['Axis'].str[3].isin([f'{letter_vertical_facade}'] ))) | equips_thing['DIN_276_Beschr.'].str.contains('External walls')|equips_thing['Axis'].str.contains('00') | equips_thing['Axis'].isin(['A58L02','A55L04'])]
    
        
        #Number of equipment not properly find because of lack of detection
        my_mistake_were_made_for_you = df1[~df1.index.isin(df2.index)]['Axis']
        v = df1[~df1.index.isin(df2.index)]
        v.to_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_equipment_mismatched_baptiste_changes.csv'), index=False)
    
        
        if not os.path.exists(os.path.join(os.getcwd(),VISUALS,'equipment_mismatching_stats.csv')):
            temps1 = pd.DataFrame(columns=[
                        'Floor',
                        'Equipment_detected',
                        'Unmatched',
                        'equipment_wall_coordinates',
                        'equipment_no_properly_placed',
                        'equipment_not_find_lack_of_coordinates'])
            temps1.to_csv(os.path.join(os.getcwd(),VISUALS,'equipment_mismatching_stats.csv'), index=False)
            temp = pd.DataFrame({
                        'Floor':floor,
                        'Equipment_detected':len(equips_thing),
                        'Unmatched':len(try_hard_fool),
                        'equipment_wall_coordinates':len(the_mother_ship),
                        'equipment_no_properly_placed':len(hey_joe),
                        'equipment_not_find_lack_of_coordinates':len(my_mistake_were_made_for_you)},index=[0])
            df = pd.concat([temps1, temp], ignore_index=True)
            df.to_csv(os.path.join(os.getcwd(),VISUALS,'equipment_mismatching_stats.csv'), index=False)
        else:
            df = pd.read_csv(os.path.join(os.getcwd(),VISUALS,'equipment_mismatching_stats.csv'))
            temp = pd.DataFrame({
                        'Floor':floor,
                        'Equipment_detected':len(equips_thing),
                        'Unmatched':len(try_hard_fool),
                        'equipment_wall_coordinates':len(the_mother_ship),
                        'equipment_no_properly_placed':len(hey_joe),
                        'equipment_not_find_lack_of_coordinates':len(my_mistake_were_made_for_you)},index=[0])
            df = pd.concat([df, temp], ignore_index=True)
            df.to_csv(os.path.join(os.getcwd(),VISUALS,'equipment_mismatching_stats.csv'), index=False)
    print('First round of coordinates matching vs equipment done.')
    return DF_MAIN