import os, datetime, sys
sys.path.append('..')

import cv2
import numpy as np
from matplotlib.path import Path

from functions.params import ROOT,PLAN_ROOT,VISUALS,PLAN_PNG


def divided_nodes_by_floor_position(floor,nodes,grid,black_background,new_resized_point1,new_resized_point2,new_resized_point3,new_resized_point4):
    """
    Function that retrieve nodes in two different part (if needed). 
    floor=str
    nodes=cv2.image
    grid=cv2.image
    black_background=cv2.image
    new_resized_points=ints
    return:
    centroids: list int.
    facade_points: list int.
    floor: list int.
    """
    contour, hier = cv2.findContours(cv2.cvtColor(nodes, cv2.COLOR_BGR2GRAY),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    centroids = []
    for cnt in contour:
        try:
            mom = cv2.moments(cnt)
            (x,y) = int(mom['m10']/mom['m00']), int(mom['m01']/mom['m00'])
            centroids.append((x,y))
        except:
            pass
    
    points = np.vstack((centroids))
    
    #Important to switch 2 and 3 to have a proper shape, else it will join the wrong dots and fill half od the picture
    ss = np.expand_dims((new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2),axis=1)
    
    p = Path((new_resized_point1,new_resized_point3,new_resized_point4,new_resized_point2)) # make a polygon
    implemntation_grid = p.contains_points(points)
    
    facade_points = []
    floor = []
    cv2.fillPoly(grid,np.int32([ss]), color=(0, 255, 0))
    for i in zip(points,implemntation_grid):
        if i[1] is np.True_:
            cv2.circle(black_background,(int(i[0][0]),int(i[0][1])),4,(0,175,255),-1)
            cv2.circle(grid,(int(i[0][0]),int(i[0][1])),4,(0,0,0),-1)
            facade_points.append((int(i[0][0]),int(i[0][1])))
        else:
            floor.append((int(i[0][0]),int(i[0][1])))
            cv2.circle(black_background,(int(i[0][0]),int(i[0][1])),4,(255,175,0),-1)
    cv2.imshow('.', black_background)
    cv2.imshow(',', grid)
    cv2.imwrite(os.path.join(os.getcwd(),VISUALS,f'{floor}',f'{floor}_DIVIDED_NODES.png'),black_background)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return centroids, floor