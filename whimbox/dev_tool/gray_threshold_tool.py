import cv2  
import numpy as np  
from whimbox.common.utils.img_utils import *
from whimbox.ui.ui_assets import *
from whimbox.interaction.interaction_core import itt

def empty(a):  
    lower = cv2.getTrackbarPos("lower", "TrackBars")  
    upper = cv2.getTrackbarPos("upper", "TrackBars")  
    return lower, upper  

cv2.namedWindow("TrackBars")  
cv2.resizeWindow("TrackBars", 640, 300)  
init_data = {
    'lower': 0,
    'upper': 255,
}
cv2.createTrackbar("lower", "TrackBars", init_data['lower'], 255, empty)  
cv2.createTrackbar("upper", "TrackBars", init_data["upper"], 255, empty)  

if __name__ == "__main__" and True:
    while True:
        lower, upper = empty(0)
        img = itt.capture()
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        _, img = cv2.threshold(img, lower, upper, cv2.THRESH_BINARY)
        cv2.imshow("img", img)
        cv2.waitKey(1)