def check_match(row, df2):
    '''Check if there is any row in df2 with the same x and y values
    row=df. Must contain ['x_axis_calculation'] and ['y_axis_calculation'] columns. Pixels coordinates and Coordinates names from Cooridnates naming
    df2=df. Must contain ['x_axis_calculation'] and ['y_axis_calculation'] columns. Room Pixels coordinates from Room Pixel function'''
    return ((df2['x_axis'] == row['x_axis']) & (df2['y_axis'] == row['y_axis'])).any()

def check_match_plus_5(row, df2):
    '''Check if there is any row in df2 with the same x and y values
    row=df. Must contain ['x_axis_calculation'] and ['y_axis_calculation'] columns. Pixels coordinates and Coordinates names from Cooridnates naming
    df2=df. Must contain ['x_axis_calculation'] and ['y_axis_calculation'] columns. Room Pixels coordinates from Room Pixel function'''
    return ((df2['x_axis'] == row['x_axis']+5) & (df2['y_axis'] == row['y_axis']+5)).any()

def check_match_plus_15_horizontal_axis(row, df2):
    '''Check if there is any row in df2 with the same x and y values
    row=df. Must contain ['x_axis_calculation'] and ['y_axis_calculation'] columns. Pixels coordinates and Coordinates names from Cooridnates naming
    df2=df. Must contain ['x_axis_calculation'] and ['y_axis_calculation'] columns. Room Pixels coordinates from Room Pixel function'''
    return ((df2['x_axis'] == row['x_axis']+5) & (df2['y_axis'] == row['y_axis']+15)).any()

def check_match_plus_15_vertical_axis(row, df2):
    '''Check if there is any row in df2 with the same x and y values
    row=df. Must contain ['x_axis_calculation'] and ['y_axis_calculation'] columns. Pixels coordinates and Coordinates names from Cooridnates naming
    df2=df. Must contain ['x_axis_calculation'] and ['y_axis_calculation'] columns. Room Pixels coordinates from Room Pixel function'''
    return ((df2['x_axis'] == row['x_axis']+15) & (df2['y_axis'] == row['y_axis']+5)).any()

def check_match_minus_10(row, df2):
    '''Check if there is any row in df2 with the same x and y values
    row=df. Must contain ['x_axis_calculation'] and ['y_axis_calculation'] columns. Pixels coordinates and Coordinates names from Cooridnates naming
    df2=df. Must contain ['x_axis_calculation'] and ['y_axis_calculation'] columns. Room Pixels coordinates from Room Pixel function'''
    return ((df2['x_axis'] == row['x_axis']-5) & (df2['y_axis'] == row['y_axis']-15)).any()