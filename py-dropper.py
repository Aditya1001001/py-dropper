import argparse
import cv2
import numpy as np
import pandas as pd

# Global variables
CLICKED = False
R = G = B = X_pos = Y_pos = 0

# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

# Reading image with opencv
image = cv2.imread(img_path)

# Reading csv file with pandas and giving names to each column
index = ["Color_Name", "Hex", "R", "G", "B"]
colors = pd.read_csv('colors.csv', names=index, header=None)


def draw_function(event, x, y, flags, param):
    '''Function that gets the x & y coordinates of the mouse clicks'''
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global R, B, G, X_pos, Y_pos, CLICKED
        CLICKED = True
        X_pos = x
        Y_pos = y
        B, G, R = image[Y_pos, X_pos]
        R = int(R)
        G = int(G)
        B = int(B)


# Creating a window to display the input image
cv2.namedWindow('Py-dropper')
# Setting a callback function to be called on mouse events
cv2.setMouseCallback('Py-dropper', draw_function)


def getColorName(r, g, b):
    ''' Takes R,G,B value of the pixel clicked on and returns the name of the color closest to it.
    (I couldn't find a better database of colors atm)'''
    min_distance = 100000
    for i in range(len(colors)):
        distance = abs(r - int(colors.loc[i, "R"])) + abs(
            g - int(colors.loc[i, "G"])) + abs(b - int(colors.loc[i, "B"]))
        if distance <= min_distance:
            min_distance = distance
            color_name = colors.loc[i, "Color_Name"]
    return color_name


while True:
    cv2.imshow("Py-dropper", image)
    if CLICKED:
        # creating a rectangle to show the color name in
        # -1 fills the rectangle 
        cv2.rectangle(image, (20, 20), (750, 60), (B, G, R), -1)
        # Creating string to display
        text = getColorName(R, G, B) + "  RGB:- (" + str(R) + "," + str(R) + "," + str(B)+ ")"

        # Displaying lighter colors in black font"
        if R+G+B >= 600:
            cv2.putText(image, text, (50, 50), 2, 0.8,
                        (0, 0, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(image, text, (50, 50), 2, 0.8,
                        (255, 255, 255), 2, cv2.LINE_AA)

        CLICKED = False
    # Breaking the loop when "esc" key is pressed
    if cv2.waitKey(10) & 0xFF == 27:
        break

cv2.destroyAllWindows()