import os, datetime, sys
sys.path.append('..')

from functions.params import ROOT,PLAN_ROOT,PLAN_PNG, VISUALS

import pandas as pd

def preprocessing_architectural_data(floor):    
    """
    Formatting Architectural Data: ECB Room size excel files
    Based on the given floor, retrieve the ecb archetectural naming plus, sorting by size for a later use.

    Input:
    floor=str. The floor used for the script. Must be spelled HN05 or HS04...

    Output:
    rooms= DF. Preprocessed ECB rooms names
    """
    
    rooms = pd.read_excel(os.path.join(ROOT,'DATA','_ECB_EXPRT-Room List =_MPE (5).xlsx'))
    rooms = rooms[(rooms['Floor Code']==f'{floor[2:]}0')&(rooms['Property code']==f'{floor[:2]}')]
    rooms['coordinates_ECB_space']=rooms['Space number'].str[7:]
    rooms = rooms.sort_values(['SP_Dimension Net'],ascending=False)

    print('preprocessing_architectural_data -Status: Done')
    
    return rooms 