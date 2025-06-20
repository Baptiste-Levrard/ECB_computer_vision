import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd
import numpy as np
import csv
from tqdm import tqdm

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

def coordinates_logical_ruling_out():
    pd.options.mode.copy_on_write = True
    
    #Third iteration to be worked on
    df_test = pd.read_csv(os.path.join(os.getcwd(),VISUALS,'equipments_to_be_moved_test.csv'))
    x = df_test[(df_test['Axis'].str[4:6].apply(lambda x: x.isdigit() and int(x) > 20))]

    DF_MAIN = pd.read_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'))
    
    for index, row in tqdm(enumerate(DF_MAIN.iterrows()),unit='Floor',total=len(DF_MAIN)):
    # Extract values from specific columns
        floor = row[1]['floor']
        letter_horizontal = row[1]['letter_horizontal']
        letter_vertical = row[1]['letter_vertical']
        letter_horizontal_facade = row[1]['letter_horizontal_facade']
        letter_vertical_facade = row[1]['letter_vertical_facade']
        CRE_to_be_added = pd.read_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_equipment_not_well_associated_CRE.csv'))
        obvious_false_vertical_coordinate = x[x['AKSfull'].str.contains(f'{floor[:2]}.{floor[-2:]}0')]
        CRE_to_be_added = pd.concat([CRE_to_be_added, obvious_false_vertical_coordinate], ignore_index=True)
        CRE_to_be_added.to_csv(os.path.join(VISUALS,f'{floor}',f'{floor}_equipment_not_well_associated_CRE.csv'), index=False)
    
    to_manual_modification_necessary = df_test[~(df_test['Axis'].str[4:6].apply(lambda x: x.isdigit() and int(x) > 20))]
    to_manual_modification_necessary.to_csv(os.path.join(os.getcwd(),VISUALS,'equipments_to_be_moved.csv'), index=False)
    return to_manual_modification_necessary