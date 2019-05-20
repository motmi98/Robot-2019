import ai2thor.controller
import numpy as np
import cv2
from pynput import keyboard
import os
import detection

def on_press(key):
    event = controller.step(dict(action='GetReachablePositions'))
    if key == keyboard.KeyCode(char='w'):
        event = controller.step(dict(action='MoveAhead', gridSize=0.2))
    elif key == keyboard.KeyCode(char='s'):
        event = controller.step(dict(action='MoveBack', gridSize=0.2))
    elif key == keyboard.KeyCode(char='a'):
        event = controller.step(dict(action='MoveLeft', gridSize=0.2))
    elif key == keyboard.KeyCode(char='d'):
        event = controller.step(dict(action='MoveRight', gridSize=0.2))
    elif key == keyboard.KeyCode(char='l'):
        event = controller.step(dict(action='RotateRight'))
    elif key == keyboard.KeyCode(char='h'):
        event = controller.step(dict(action='RotateLeft'))
    elif key == keyboard.KeyCode(char='k'):
        event = controller.step(dict(action='LookUp'))
    elif key == keyboard.KeyCode(char='j'):
        event = controller.step(dict(action='LookDown'))
    elif key == keyboard.KeyCode(char='c'):
    	object_detection(event)
 

def on_release(key):
    if key == keyboard.Key.esc:
        return False

"""
def pick_object(event):
	object_id = ''
	for aval_object in event.metadata['objects']:
		object_id = aval_object['objectId']
	return controller.step(dict(action='PickupObject', objectId=object_id))

def put_object(event):
	object_id = ''
	receptacle_id = ''
	for rec_object in event.metadata['objects']:
		if rec_object['receptacle']:
			receptacle_id = rec_object['objectId']
	for aval_object in event.metadata['objects']:
		object_id = aval_object['objectId']
	return controller.step(dict(action='PutObject', objectId=object_id, receptacleObjectId=receptacle_id, placeStationery=False, forceAction=False))
"""

def get_frame(event):
	frame = event.cv2img
	cv2.imwrite("image.jpg", frame)
	return frame

def show_image(image):
	cv2.namedWindow('image', cv2.WINDOW_NORMAL)
	cv2.imshow('prediction', image)
	cv2.waitKey(32)
	cv2.destroyAllWindows()

def object_detection(event):
	frame = event.cv2img
	cv2.imwrite("image.jpg", frame)
	detection.detect("image.jpg")

controller = ai2thor.controller.Controller()
controller.start(player_screen_width=1000, player_screen_height=700)
controller.reset('FloorPlan28')
controller.step(dict(action='Initialize', gridSize=0.25))

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
