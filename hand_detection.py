# IMPORTING LIBRARIES
import cv2
import cvzone

from cvzone.HandTrackingModule import HandDetector
from picamera2 import Picamera2

picam2 = Picamera2()

import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import time


# SETTINGS
picam2.preview_configuration.main.size = (640, 480)
width, height = 640, 480
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.start()
detector = HandDetector(maxHands=2, detectionCon=0.5, minTrackCon=0.5)

time.sleep(2)

# Initialize time variables for FPS
pTime = 0  # previous time
cTime = 0  # current time

while True:
    # captures each frame of the preview as an image
    im = picam2.capture_array()

    # Detect hands
    hands, im = detector.findHands(im, draw=True)

    # (Optional) Do your finger-states logic here...

    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display FPS on the frame
    cv2.putText(
        im, 
        f"FPS: {int(fps)}", 
        (10, 30), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, 
        (255, 0, 0), 
        2
    )

    # Create an OpenCV window to show the hand detection
    cv2.imshow("im", im)

    # if 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
picam2.stop()