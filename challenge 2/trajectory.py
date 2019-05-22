import math
import matplotlib.pyplot as plt
from ai2thor.controller import Controller
from PIL import Image, ImageDraw
import numpy as np
import keyboard

stages = [] 

class converter(object):
    def __init__(self, frame_shape, cam_position, orth_size):
        self.frame_shape = frame_shape
        self.lower_left = np.array((cam_position[0], cam_position[2])) - orth_size
        self.span = 2 * orth_size

    def __call__(self, position):
        if len(position) == 3:
            x, _, z = position
        else:
            x, z = position

        camera_position = (np.array((x, z)) - self.lower_left) / self.span
        return np.array(
            (
                round(self.frame_shape[0] * (1.0 - camera_position[1])),
                round(self.frame_shape[1] * camera_position[0]),
            ),
            dtype=int,
        )

def get_position(position):
    return (position["x"], position["y"], position["z"])

def get_agent_map_data(c: Controller):
    c.step(dict(action = 'ToggleMapView'))
    cam_position = c.last_event.metadata["cameraPosition"]
    cam_orth_size = c.last_event.metadata["cameraOrthSize"]
    pos_converted = converter(
        c.last_event.frame.shape, get_position(cam_position), cam_orth_size
    )
    to_return = {
        "frame": c.last_event.frame,
        "cam_position": cam_position,
        "cam_orth_size": cam_orth_size,
        "pos_converted": pos_converted
    }
    c.step(dict(action = 'ToggleMapView'))
    return to_return

def draw(position, rotation, frame, pos_converted, c:Controller):
    global stages
    previous_image = Image.fromarray(frame.astype("uint8"), "RGB").convert("RGBA")
    new_image = Image.new("RGBA", frame.shape[:-1]) 
    convert = pos_converted(position)
    figure = ImageDraw.Draw(new_image)  
    if c.last_event.metadata['lastActionSuccess'] == True:
    	z = stages[-1][0]
    	x = stages[-1][1]
    	if z != (convert[1] - 5, convert[0] - 5)  or x != (convert[1] + 5, convert[0] + 5):
    		stages += [((convert[1] - 5, convert[0] - 5), (convert[1] + 5, convert[0] + 5))]

    for index in range(len(stages)):
    	figure.rectangle((stages[index][0], stages[index][1]), fill='red')
        
    image = Image.alpha_composite(previous_image, new_image)
    return np.array(image.convert("RGB"))

if __name__ == "__main__":    
    controller = Controller()
    controller.start()
    controller.reset("FloorPlan24")
    controller.step(dict(action = 'Initialize', gridSize = 0.2))
    top_view = get_agent_map_data(controller)
    convert = top_view["pos_converted"](get_position(controller.last_event.metadata["agent"]["position"]))
    stages += [((convert[1] - 5, convert[0] - 5), (convert[1] + 5, convert[0] + 5))]
    frame = draw(
        get_position(controller.last_event.metadata["agent"]["position"]),
        controller.last_event.metadata["agent"]["rotation"]["y"],
        top_view["frame"],
        top_view["pos_converted"],
        controller
    )   
    
    plt.ion()
    plt.imshow(frame)
    plt.show()
    while True:
        if keyboard.is_pressed('left arrow'):
            plt.clf()
            event = controller.step(dict(action = 'MoveLeft'))
        elif keyboard.is_pressed('right arrow'):
            plt.clf()
            event = controller.step(dict(action = 'MoveRight'))
        elif keyboard.is_pressed('up arrow'):
            plt.clf()
            event = controller.step(dict(action = 'MoveAhead'))
        elif keyboard.is_pressed('down arrow'):
            plt.clf()
            event = controller.step(dict(action = 'MoveBack'))
        elif keyboard.is_pressed('l'):
            plt.clf()
            event = controller.step(dict(action = 'RotateRight'))
        elif keyboard.is_pressed('h'):
            plt.clf()
            event = controller.step(dict(action = 'RotateLeft'))
        elif keyboard.is_pressed('k'):
            plt.clf()
            event = controller.step(dict(action = 'LookUp'))
        elif keyboard.is_pressed('j'):
            plt.clf()
            event = controller.step(dict(action = 'LookDown'))
        elif keyboard.is_pressed('esc'):
            break
        frame = draw(
            get_position(controller.last_event.metadata["agent"]["position"]),
            controller.last_event.metadata["agent"]["rotation"]["y"],
            top_view["frame"],
            top_view["pos_converted"],
            controller
        )
        plt.imshow(frame)
        plt.show()
        plt.pause(0.001)