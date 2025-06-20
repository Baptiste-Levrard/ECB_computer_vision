#pip install opencv-python
import cv2
#Helping tool
#Way less moody since the changes.
#Mannually select the colours
def nothing(x):
    pass

# Load image
image_path = 'Plan_04_OPTI_90D_CROPPED.png'
image = cv2.imread(image_path)

# Create a window
cv2.namedWindow('result')

# Create trackbars for color change
# Hue is from 0-179 for OpenCV
cv2.createTrackbar('HMin', 'result', 0, 179, nothing)
cv2.createTrackbar('SMin', 'result', 0, 255, nothing)
cv2.createTrackbar('VMin', 'result', 0, 255, nothing)
cv2.createTrackbar('HMax', 'result', 0, 179, nothing)
cv2.createTrackbar('SMax', 'result', 0, 255, nothing)
cv2.createTrackbar('VMax', 'result', 0, 255, nothing)

# Set default value for Max HSV trackbars
cv2.setTrackbarPos('HMax', 'result', 179)
cv2.setTrackbarPos('SMax', 'result', 255)
cv2.setTrackbarPos('VMax', 'result', 255)

# Initialize HSV min/max values
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

while True:
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'result')
    sMin = cv2.getTrackbarPos('SMin', 'result')
    vMin = cv2.getTrackbarPos('VMin', 'result')
    hMax = cv2.getTrackbarPos('HMax', 'result')
    sMax = cv2.getTrackbarPos('SMax', 'result')
    vMax = cv2.getTrackbarPos('VMax', 'result')

    # Set minimum and maximum HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Convert to HSV format and color threshold
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)

    # Print if there is a change in HSV value
    #if (phMin != hMin) or (psMin != sMin) or (pvMin != vMin) or (phMax != hMax) or (psMax != sMax) or (pvMax != vMax):
    #   print(f'hMin = {hMin}, sMin = {sMin}, vMin = {vMin}, hMax = {hMax}, sMax = {sMax}, vMax = {vMax}')
    #    phMin = hMin
    #    psMin = sMin
    #    pvMin = vMin
    #    phMax = hMax
    #    psMax = sMax
    #    pvMax = vMax

    # Display result image
    cv2.imshow('result', result)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Esc key to stop
        break

cv2.destroyAllWindows()