#Importing usual libraries
import os, sys, datetime, argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#Import projects parameters
from functions.params import ROOT,PLAN_ROOT,PLAN_PNG

#Importing project functions
from functions.rooms_coordinates_equipment_coordinates_matching import rooms_coordinates_equipment_coordinates_matching
from functions.coordinates_mathematical_finding import coordinates_mathematical_finding
from functions.coordinates_logical_ruling_out import coordinates_logical_ruling_out
from functions.computing_pixels_matching_calculated_coordinates import computing_pixels_matching_calculated_coordinates

#Importing projects' support fuctions
from functions.pixel_matching_support_functions import *

parser = argparse.ArgumentParser(description='Visual verification - Plotted coordinates')
parser.add_argument('--auto_complete', help='str. Show the plotted coordinate axis. e.g. yes/no', required=True, type=str)
args = parser.parse_args()


if __name__ == '__main__':

    auto_complete = args.auto_complete
    
    fourth_and_Roebling = rooms_coordinates_equipment_coordinates_matching()
    riptide = coordinates_mathematical_finding()
    going_gets_tough = coordinates_logical_ruling_out()
    dream = computing_pixels_matching_calculated_coordinates(auto_complete)