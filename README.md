# Room/Equipment Matching Using Computer Vision: Project Guide

This guide provides an overview and instructions for using the Room/Equipment Matching project. This project leverages computer vision to analyze CAD architectural plans, extract room data, and match it with equipment data.

Note: All ECB data has been removed from the following folders.

## 1. Project Overview
### 1.1 Project Name

Room/Equipment Matching: Computer Vision Use Case

### 1.2 Objective & Benefits

This project aims to:

Analyze CAD architectural plans for each floor of main buildings.
Retrieve room area and coordinates.
Match equipment positions (from Planon) to corresponding rooms.
Align ECB room names with the correct rooms using computer vision.

Beneficiaries: 

This project enhances data quality and reporting capabilities for facility management and planning.

### 1.3 Key Metrics & Improvements

Data Quality: Improve Planon's equipment data quality by accurately associating it with rooms.
Reporting & Speed: Generate faster and more accurate visualizations of floor layouts.
Accuracy Enhancement: Focus on improving the room_naming_and_links.py script to achieve higher accuracy in room-equipment matching.

### 1.4 Deliverables

Accurate room-to-equipment mappings.
Visualizations of floor layouts, including 2D representations and equipment scatter plots.
Consolidated data files for streamlined analysis.

## 2. Data Management
### 2.1 Data Locations

Darwin: Organized folders for storing raw (floors, rooms, equipment) and processed floor data.
GitLab: Project repository containing CAD plans and all project scripts.
Planon: Primary source for equipment data.

### 2.2 Data Cleaning

The following folders have been emptied from all the ECB Data.


## 3. Dependencies
### 3.1 Poetry Dependency Management

Poetry is used for managing project dependencies.

    Install Poetry (if not already installed):
    Bash
    conda install poetry


Navigate to the project directory:

    Bash
    cd /path/to/your/project


Install project dependencies:

    Bash
    poetry install

Note: Ensure the pyproject.toml file exists in the directory. If poetry.lock does not exist, Poetry will generate it automatically.

### 3.2 Additional Dependencies

For ECB-related Python packages, install them using your preferred package manager (e.g., pip or conda).

## 4. Script Usage
   
The project comprises three main processing scripts and one utility function for data aggregation.
   
### 4.1 Pre-processing Floor Plans

    Script: pre_processing_floor_plan.py
    Purpose: Process ECB architectural plans to extract pixel coordinates of rooms.
    Input:
        CAD plans in .pdf format (located in the Plans folder).
            North Building Plans:
                ASPART-9-ECBCS-{floor}0-oooooo-G-BAJ001-000000 Grid.pdf
                ASPART-9-ECBCS-{floor}0-oooooo-G-BAJ001-000000 Model.pdf
            South Building Plans:
                ASPART-9-ECBCS-HS-{floor}0-oooooo-G-BAJ001-000000 Grid.pdf
                ASPART-9-ECBCS-HS-{floor}0-oooooo-G-BAJ001-000000 Model.pdf
        User-Defined Variables: The script will prompt for the following variables during execution:
            floor (str)
            letter_horizontal (str)
            letter_vertical (str)
            letter_horizontal_facade (str)
            letter_vertical_facade (str)
            angle1 (float)
            angle2 (float)
            min_size_trapeze_line (int)
            x (int)
            y (int)
            angle_calculation (int)
            area_threshold (float)
            vertex_threshold (int)
            number_false_room (int)
            area_threshold_bigger_rooms (int)
            bbox_area (float)
            aspect_ratio_threshold (float)
            balcony_area_detected (int)
            number_false_room_transfer (int)
            number_balcony_transfer_room (int)
            angle_floor (int)
            tolerance_x_floor (int)
            tolerance_y_floor (int)
            y_threshold_floor (int)
            a_index_floor (int)
            angle_facade (float)
            tolerance_x_facade (int)
            tolerance_y_facade (int)
            y_threshold_facade (int)
            n_index_facade (int)
    Output: .csv files containing pixel coordinates for rooms, nodes, and computer vision-detected rooms.

### 4.2 Refining Pixel Coordinates

    Script: refining_pixels_coordinates.py
    Purpose: Improve computer vision results using mathematical functions and incorporate manual ECB inputs/corrections.
    Input: Overall hyperparameter .csv file.
    Execution: Run the script for all floors in the input file using:

    python refining_pixels_coordinates.py --auto_complete=yes

    Output: Refined .csv files with updated pixel coordinates and associated rooms.

### 4.3 Room Naming and Links

    Script: room_naming_and_links.py
    Purpose: Match computer vision-detected room coordinates with ECB-defined room names and visualize the results.
    Input: Floor name (e.g., HS04).
    Execution:

    python room_naming_and_links.py --floor HS04

    Output: .csv files containing room-equipment mappings and coordinate details.

### 4.4 Final Data Aggregation

    Utility Function: functions.ROOM_NAMING.final_df_concatination
    Purpose: Combine all generated .csv files into a single Excel (.xlsx) file for easier analysis and access.
    Output: A consolidated .xlsx file containing all relevant project data.

## 5. Visualizations

Work is ongoing to develop enhanced floor visualizations, including:

    2D visualizations highlighting detected rooms.
    Scatter plots illustrating equipment positions within floor layouts.
