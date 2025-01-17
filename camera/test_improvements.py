# copied over from Confluence Landmark Detection Code and Pseudocode (just wrote it to help me understand the code)

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
fps = 0
prev_time = time.time()


# SETTINGS
# setting picamera screen size, data format(RGB) and aligning preview config for efficient real-time preview
picam2.preview_configuration.main.size = (640, 480)

width, height = 640, 480

picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()

# starting picamera preview & entering settings for HandDetector
picam2.start()
detector = HandDetector(maxHands = 2, detectionCon = 0.5, minTrackCon = 0.5)
	# creating an instance of the HandDetector with custom arguments -> detects hands in the current frame

list = [] # Q: what is this for

# adding time for picamera to activate (prevents overheating & improves preview quality)
time.sleep(2)

# WHILE
while True:
	# captures each frame of the preview as an image (variable name is im, im is the input image/frame)
	im = picam2.capture_array()
	#im = cv2.flip(im_original, 1) # flipping horizontally -> this flips the handedness (nvm)
	
	# use detector from HandDetector to find hands and draw the landmarks on the hand
	hands, im = detector.findHands(im, draw = True)
	
	# FINGERS UP OR DOWN -> only works with one hand at a time right now
	if len(hands)==1: 
		
		first_hand = hands[0] # first hand that gets in frame
		
		handedness = first_hand['type']
		print(f"{handedness} hand is in frame")
		
		lmlist = first_hand['lmList'] # gets landmark list (EVERY landmark) from the first hand in the frame
		
		finger_states = []
		
		# "origin" on screen is bottom left (like a graph)
		
		# THUMB
		# note: thumb is annoying because they might do a thumbs up & flip their hand inwards/outwards which messes with the thumb in/out thing
		# i couldn't not implement the thumb in/out thing because someone's thumb might be upright but folded inwards (meaning "down")
		# unless we do something with the palm?
		thumb_tip_y = height - lmlist[4][1]
		thumb_tip_x = lmlist[4][0]
		
		thumb_knuckle_y = height - lmlist[3][1] # using first knuckle for thumb (idk why ngl)
		thumb_knuckle_x = lmlist[3][0]
		
		# print(f"Thumb: tip=({thumb_tip_x},{thumb_tip_y}), thumb_knuckle=({thumb_knuckle_x},{thumb_knuckle_y})")
		
		if handedness == 'Right':
			if thumb_tip_x < thumb_knuckle_x or thumb_tip_y < thumb_knuckle_y : #right thumb down or in means thumb = down
				thumb_state = "Down"
			else: # else thumb = up
				thumb_state = "Up"
		else:
			if thumb_tip_x > thumb_knuckle_x or thumb_tip_y < thumb_knuckle_y : 
				thumb_state = "Down"
			else: 
				thumb_state = "Up"
		
		finger_states.append(thumb_state) # add the state of thumb to the list
		#print(f"{handedness} thumb {thumb_state}")
		
		# OTHER FINGERS
		finger_tips = [8, 12, 16, 20] # note: didnt include thumb as it's a little different
		finger_knuckles = [6, 10, 14, 18] # using second knuckle for other fingers (fist situation)
		
		for tip, knuckle in zip(finger_tips, finger_knuckles): # iterates through each pair of indices: (4,3) (8,7) etc
			
			if tip == 8:
				finger = "Index"
			elif tip == 12:
				finger = "Middle"
			elif tip == 16:
				finger = "Ring"
			elif tip == 20:
				finger = "Pinky"
			
			tip_x = lmlist[tip][0]
			tip_y = height - lmlist[tip][1] # correcting y-coor: as you go UP, corrected y-coor increases
			
			knuckle_x = lmlist[knuckle][0]
			knuckle_y = height - lmlist[knuckle][1]
			
			# print(f"{tip}: tip=({tip_x},{tip_y}), knuckle=({knuckle_x},{knuckle_y})") # debugging
			
			if (tip_y) > (knuckle_y): # tip above first knuckle finger = up, otherwise finger = down
				finger_state = "Up"
			else:
				finger_state = "Down"
			
			finger_states.append(finger_state) # add the state of other fingers to the list
			#print(f"{finger} finger {finger_state}")
			
			
		print(f"Finger states: {finger_states}") # print finger states after the loop
		
		if finger_states == ["Down", "Up", "Down", "Down", "Down"]:
			gesture = "Point"
		elif finger_states == ["Down", "Up", "Up", "Down", "Down"]:
			gesture = "Peace"
		elif finger_states == ["Down", "Up", "Up", "Up", "Down"]:
			gesture = "Three"
		elif finger_states == ["Down", "Up", "Up", "Up", "Up"]:
			gesture = "Four"
		elif finger_states == ["Up", "Up", "Up", "Up", "Up"]:
			gesture = "High five"
		elif finger_states == ["Down", "Down", "Down", "Down", "Down"]:
			gesture = "Fist"
		elif finger_states == ["Down", "Up", "Down", "Down", "Up"]:
			gesture = "Rock on"
		elif finger_states == ["Up", "Down", "Down", "Down", "Down"]:
			gesture = "Thumbs up" # note: might not always work
		elif finger_states == ["Up", "Down", "Down", "Down", "Up"]:
			gesture = "Call"
		else:
			gesture = "None"
		
		#print(f"Gesture: {gesture}!")
	
	#record the current time after taking prev time from last frame
	curr_time = time.time()
	#The amount of time per frame
	time_diff = curr_time - prev_time
	fps = 1/time_diff if time_diff > 0 else 0
	#updates for next frame
	prev_time = curr_time
	print("fps: ", fps)
	#display on screen
	#cv2.putText(im, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
	
	
	# to create an opencv window to show the hand detection
	cv2.imshow("im", im)
	
	# if q is pressed, stop previewing & exit while loop
	if cv2.waitKey(1) & 0xFF == ord('q'): # note: pressing q doesn't exit the program after making terminal print info (like x/y coor, etc) -> had to ctrl C -> 
		break

# EXITING	
# close all opencv windows to clear up data & files created over the previewing & detection process
cv2.destroyAllWindows()

# stop the picamera preview
picam2.stop()

