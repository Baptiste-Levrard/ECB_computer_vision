import os, sys, datetime, argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np

#Import projects parameters
from functions.params import ROOT,PLAN_ROOT,PLAN_PNG,VISUALS

def overall_hyperparameters_big_rooms_floors_computer_vision(floor,big_room_variable):
    df = pd.read_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'))
    
    cc = df[df['floor']==floor]
    cc['top_rooms']= big_room_variable
    
    df = df[df['floor'] != floor]
    df = pd.concat([df, cc], ignore_index=True)

    df.to_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'), index=False)
    print('overall_hyperparameters_floors_computer_vision.csv has been updated')
    return df