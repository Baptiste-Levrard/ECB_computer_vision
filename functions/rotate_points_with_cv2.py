import os, sys, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import cv2

def rotate_points_with_cv2(points, M):
    # Convert the list of points to a numpy array with shape (n, 2)
    points_array = np.array(points, dtype=np.int32)

    # Convert points to homogeneous coordinates by adding a column of ones
    ones = np.ones((points_array.shape[0], 1), dtype=np.int32)
    points_homogeneous = np.hstack([points_array, ones])

    # Apply the rotation matrix
    rotated_points_homogeneous = points_homogeneous.dot(M.T)

    # Extract the x, y coordinates from the homogeneous coordinates
    rotated_points = rotated_points_homogeneous[:, :2].astype(int)

    return rotated_points