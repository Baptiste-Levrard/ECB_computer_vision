README: Room/Equipment Matching Using Computer Vision
This project aims to analyze CAD architectural plans of building floors, retrieve room data, and match it with equipment data using computer vision. The process involves cleaning data, extracting room coordinates, associating equipment to rooms, and producing visualizations. Below, you will find an organized guide for using the project scripts and understanding the workflow.

1. Project Overview
2. 
1.1 Project Name
Room/Equipment Matching: Computer Vision Use Case

1.2 Objective & Beneficiary

Analyze CAD architectural plans for each floor of main buildings.
Retrieve the area and coordinates of rooms.
Match equipment positions from Planon to rooms.
Align ECB room names to the correct rooms using computer vision.

1.3 Key Metrics

Data Cleaning and Quality: Improve Planon’s data quality.
Reporting and Speed: Develop faster and more accurate visualizations for floor layouts.
Improvements: Focus on fixing the room_naming_and_links.py script for better accuracy in room-equipment matching.

1.4 Deliverables

Accurate room-to-equipment mapping.
Visualizations of floor layouts, including 2D visualizations and scatter plots of equipment.
Consolidated data files for easier analysis.

2. Data Storage

2.1 Locations

Darwin: Organized folders for floors, rooms, equipment, and processed floor data.
Darwin Link
GitLab: Repository containing CAD plans and scripts.
Planon: Source of equipment data.

3. Project Administrators

4. 
Almeida Fernando
Comoretto Luca
Menghelin Sebastiano

5. Dependencies

4.1 Poetry Dependency Management
Install Poetry using Conda:
conda install poetry
Navigate to the project directory.
Install project dependencies:
poetry install
(Note: Ensure the pyproject.toml file exists before running this command. If the poetry.lock file does not exist, Poetry will automatically generate it.)

4.2 Additional Dependencies
For ECB-related Python packages, install them using your preferred package manager (e.g., pip or conda).

5. Scripts Usage
The project consists of 3 main scripts and 1 utility function for data aggregation.

5.1 Pre-processing Floor Plans
Script: pre_processing_floor_plan.py
Purpose: Process ECB architectural plans to retrieve pixel coordinates of rooms.
Input:

CAD plans in .pdf format (located in the Plans folder).
North Building Plans:
ASPART-9-ECBCS-{floor}0-oooooo-G-BAJ001-000000 Grid.pdf
ASPART-9-ECBCS-{floor}0-oooooo-G-BAJ001-000000 Model.pdf
South Building Plans:
ASPART-9-ECBCS-HS-{floor}0-oooooo-G-BAJ001-000000 Grid.pdf
ASPART-9-ECBCS-HS-{floor}0-oooooo-G-BAJ001-000000 Model.pdf
User-defined variables (these will be prompted during script execution):
floor=str
letter_horizontal=str
letter_vertical=str
letter_horizontal_facade=str
letter_vertical_facade=str
angle1=float
angle2=float
min_size_trapeze_line=int
x=int
y=int
angle_calculation=int
area_threshold=float
vertex_threshold=int
number_false_room=int
area_threshold_bigger_rooms=int
bbox_area=float
aspect_ratio_threshold=float
balcony_area_detected=int
number_false_room_transfer=int
number_balcony_transfer_room=int
angle_floor=int
tolerance_x_floor=int
tolerance_y_floor=int
y_threshold_floor=int
a_index_floor=int
angle_facade=float
tolerance_x_facade=int
tolerance_y_facade=int
y_threshold_facade=int
n_index_facade=int
Output:
.csv files with pixel coordinates for rooms, nodes, and computer vision-detected rooms.

5.2 Refining Pixel Coordinates
Script: refining_pixels_coordinates.py
Purpose: Improve computer vision results using mathematical functions and handle manual ECB input/mistakes.
Input:

Overall hyperparameter .csv file.
Run the script for all floors in the file using:
--auto_complete=yes
Output:
Refined .csv files with pixel coordinates and associated rooms.

5.3 Room Naming and Links
Script: room_naming_and_links.py
Purpose: Match computer vision coordinates with ECB-defined room names and visualize the results.
Input:

Floor name (e.g., HS04):
--floor HS04
Output:
.csv files with room-equipment mappings and coordinate details.

5.4 Final Data Aggregation
Utility Function: final_df_concatination.py
Location: functions.ROOM_NAMING.final_df_concatination
Purpose: Combine all .csv files into a single Excel file for easier access.
Output:

Consolidated .xlsx file with all relevant data.

6. Visualizations
Efforts are underway to create better floor visualizations, such as:

2D visualizations highlighting rooms.
Scatter plots showing equipment positions.

7. Jira Tickets
This project is tracked under Jira ticket:

DGAFSA-1276 - Vision-Based Equipment-Room Mapping in Floor Layouts.

8. Known Issues
The room_naming_and_links.py script does not yet provide 100% correct results for all floors. Improvements are being made iteratively.
Pre-processing functions may need adaptation for specific floors (e.g., HN27, HS14, HS38).

For any questions or issues, please contact the project administrators.