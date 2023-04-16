import numpy as np 
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv2.imshow('Webcam Test', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break