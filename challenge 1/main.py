import ai2thor.controller
import numpy as np
import cv2
from pynput import keyboard
import os
import detection
import trajectory
import matplotlib.pyplot as plt

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
		print("Detecting object . . .")
		object_detection(event)

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def draw():
	new_frame = test.draw(
		test.position_to_tuple(controller.last_event.metadata["agent"]["position"]),
		controller.last_event.metadata["agent"]["rotation"]["y"],
		top_view["frame"],
		top_view["pos_translator"],
	    controller
	)
	plt.imshow(new_frame)
	plt.show()
	plt.pause(0.001)

def object_detection(event):
	frame = event.cv2img
	cv2.imwrite("image.jpg", frame)
	detection.detect("image.jpg")

if __name__ == "__main__":	
	controller = ai2thor.controller.Controller()
	controller.start(player_screen_width=1000, player_screen_height=700)
	controller.reset('FloorPlan24')
	controller.step(dict(action='Initialize', gridSize=0.25))
	with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
	    listener.join()
	