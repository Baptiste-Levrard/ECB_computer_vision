import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import cv2
import pandas as pd
import csv
from tqdm import tqdm

from functions.params import ROOT,PLAN_ROOT,VISUALS,PLAN_PNG
from functions.pixels_matching_calculated_coordinates import pixels_matching_calculated_coordinates

def computing_pixels_matching_calculated_coordinates(auto_complete):
    pd.options.mode.copy_on_write = True
    
    DF_MAIN = pd.read_csv(os.path.join(os.getcwd(),VISUALS,'overall_hyperparameters_floors_computer_vision.csv'))
    
    for index, row in tqdm(enumerate(DF_MAIN.iterrows()),unit='Floor',total=len(DF_MAIN)):
    # Extract values from specific columns
        floor = row[1]['floor']
        pixels_matching_calculated_coordinates(auto_complete,floor)
    return DF_MAIN