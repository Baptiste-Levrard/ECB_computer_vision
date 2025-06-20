import os, datetime, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pdf2image import convert_from_path
import cv2

from functions.params import ROOT,PLAN_ROOT,VISUALS,PLAN_PNG

def retrieve_pdf(floor):
    """
    Retrieve the DWG file converted to pdf and save it as png.
    You have to be careful to follow the required format and name calling.
    Pass the correct 
    """
    number = floor[-2:]
    if 'HN' in floor: 
        plan = f'ASPART-9-ECBCS-{number}0-oooooo-G-BAJ001-000000 Model.pdf'
    elif 'HS' in floor:
        plan = f'ASPART-9-ECBCS-HS-{number}0-oooooo-G-BAJ001-000000 Model.pdf'
        
    plan_name_wo_extension = plan[:-4]
    grid = plan[:-9] + 'Grid'
    grid_pdf = grid +'.pdf'
    
    pages = convert_from_path(os.path.join(PLAN_ROOT,plan))
    grid_pages = convert_from_path(os.path.join(PLAN_ROOT,grid_pdf))

    if not os.path.exists(os.path.join(VISUALS,floor)):
        os.mkdir(os.path.join(VISUALS,floor))
    
    for page in range(len(pages)):
        pages[page].save(os.path.join(PLAN_ROOT,f"{floor}-{plan_name_wo_extension}.png"))
        
    for page in range(len(grid_pages)):
        grid_pages[page].save(os.path.join(PLAN_ROOT,f"{floor}-{grid}.png"))
        
        return cv2.imread(os.path.join(PLAN_ROOT,f"{floor}-{plan_name_wo_extension}.png")), cv2.imread(os.path.join(PLAN_ROOT,f"{floor}-{grid}.png"))