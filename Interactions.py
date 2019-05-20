from pynput import keyboard
import ai2thor.controller
import numpy as np
import cv2
import os
import Yolo
import time

#to move left: action='MoveLeft'
#to move right: action='MoveRight'
#to move forward: action='MoveAhead'
#to move backwards: action='MoveBack'


list = []
start = 0
heldObject = ''
directions = ['MoveAhead', 'MoveLeft', 'MoveRight', 'MoveBack']


def dfs(ev, test):
    for obj in ev.metadata['objects']:
        if obj['name'] == test:
            dist = obj['distance']
    while dist > 1:
        if dist not in list:
            list.append(dist)
            for string in directions:
                dfs(controller.step(dict(action=string)))
        else:
            break
    if ev.metadata['lastAction'] == 'MoveLeft':
        controller.step(dict(action='MoveRight'))
    elif ev.metadata['lastAction'] == 'MoveRight':
        controller.step(dict(action='MoveLeft'))
    elif ev.metadata['lastAction'] == 'MoveAhead':
        controller.step(dict(action='MoveBack'))


def min_dist(test):
    dists = []
    minimum = np.Inf
    while True:
        for string in directions:
            for obj in controller.step(dict(action=string)).metadata['objects']:
                if obj['name'] == test:
                    dists.append(obj['distance'])
                    print(string, obj['distance'])
        for i in dists:
            if i == minimum:
                i = np.Inf
        min1 = np.minimum(dists[0], dists[1])
        min2 = np.minimum(min1, dists[2])
        min3 = np.minimum(min2, dists[3])
        minimum = min3
        if minimum in list:
            break
        else:
            list.append(minimum)
        if minimum == dists[0]:
            controller.step(dict(action='MoveAhead'))
        elif minimum == dists[1]:
            controller.step(dict(action='MoveLeft'))
        elif minimum == dists[2]:
            controller.step(dict(action='MoveRight'))
        elif minimum == dists[3]:
            controller.step(dict(action='MoveBack'))
        dists.clear()


def on_press(key):
    global start
    event = controller.step(dict(action='GetReachablePositions'))
    if key == keyboard.Key.up:
        event = controller.step(dict(action='MoveAhead', gridSize=0.2))
    elif key == keyboard.Key.down:
        event = controller.step(dict(action='MoveBack', gridSize=0.2))
    elif key == keyboard.Key.left:
        event = controller.step(dict(action='MoveLeft', gridSize=0.2))
    elif key == keyboard.Key.right:
        event = controller.step(dict(action='MoveRight', gridSize=0.2))
    elif key == keyboard.KeyCode(char='d'):
        event = controller.step(dict(action='RotateRight'))
    elif key == keyboard.KeyCode(char='a'):
        event = controller.step(dict(action='RotateLeft'))
    elif key == keyboard.KeyCode(char='w'):
        event = controller.step(dict(action='LookUp'))
    elif key == keyboard.KeyCode(char='s'):
        event = controller.step(dict(action='LookDown'))
    elif key == keyboard.KeyCode(char='i'):
        event = pick_up(event)
    elif key == keyboard.KeyCode(char='u'):
        event = put_down(event)
    elif key == keyboard.KeyCode(char='j'):
        event = controller.step(dict(action='DropHandObject'))
    elif key == keyboard.KeyCode(char='k'):
        if start == 0:
            start = time.time()
    elif key == keyboard.KeyCode(char='o'):
        event = open_object(event)
    elif key == keyboard.KeyCode(char='l'):
        event = close_object(event)
    elif key == keyboard.KeyCode(char='n'):
        event = turn_on(event)
    elif key == keyboard.KeyCode(char='m'):
        event = turn_off(event)
    draw_object_bounds(event)


def on_release(key):
    event = controller.step(dict(action='GetReachablePositions'))
    global stop
    global start
    if key == keyboard.KeyCode(char='k'):
        stop = time.time()
        print(stop-start)
        event = controller.step(dict(action='ThrowObject', moveMagnitude=(stop-start)*100))
        start = 0
    draw_object_bounds(event)


def put_down(event):
    minimum = np.Inf
    objectId = ''
    for obj in event.metadata['objects']:
        if obj['distance'] < minimum:
            minimum = obj['distance']
            objectId = obj['objectId']
    minimum = np.Inf
    receptacleId = ''
    for obj in event.metadata['objects']:
        if obj['receptacle']:
            if obj['distance'] < minimum:
                minimum = obj['distance']
                receptacleId = obj['objectId']
    return controller.step(dict(action='PutObject', objectId=objectId, receptacleObjectId=receptacleId,
                                placeStationery=False, forceAction=True))


def pick_up(event):
    minimum = np.Inf
    objectId = ''
    for obj in event.metadata['objects']:
        if obj['distance'] < minimum:
            minimum = obj['distance']
            objectId = obj['objectId']
    return controller.step(dict(action='PickupObject', objectId=objectId))


def open_object(event):
    minimum = np.Inf
    objectId = ''
    for obj in event.metadata['objects']:
        if obj['distance'] < minimum and obj['distance'] < 1.5:
            minimum = obj['distance']
            objectId = obj['objectId']
    if minimum < 1.5:
        return controller.step(dict(action='OpenObject', objectId=objectId))
    else:
        return controller.step(dict(action='GetReachablePositions'))


def close_object(event):
    minimum = np.Inf
    objectId = ''
    for obj in event.metadata['objects']:
        if obj['distance'] < minimum and obj['distance'] < 1.5:
            minimum = obj['distance']
            objectId = obj['objectId']
    if minimum < 1.5:
        return controller.step(dict(action='CloseObject', objectId=objectId))
    else:
        return controller.step(dict(action='GetReachablePositions'))


def turn_on(event):
    minimum = np.Inf
    objectId = ''
    for obj in event.metadata['objects']:
        if obj['distance'] < minimum and obj['distance'] < 1.5:
            minimum = obj['distance']
            objectId = obj['objectId']
    if minimum < 1.5:
        return controller.step(dict(action='ToggleObjectOn', objectId=objectId))
    else:
        return controller.step(dict(action='GetReachablePositions'))


def turn_off(event):
    minimum = np.Inf
    objectId = ''
    for obj in event.metadata['objects']:
        if obj['distance'] < minimum and obj['distance'] < 1.5:
            minimum = obj['distance']
            objectId = obj['objectId']
    if minimum < 1.5:
        return controller.step(dict(action='ToggleObjectOff', objectId=objectId))
    else:
        return controller.step(dict(action='GetReachablePositions'))


def draw_object_bounds(ev):
    frame = ev.cv2img
    cv2.imwrite("image.jpg", frame)
    for obj in ev.metadata['objects']:
        for key in ev.instance_detections2D.keys():
            if obj['objectId'] == key:
                x = ev.instance_detections2D.get(key)[0]
                y = ev.instance_detections2D.get(key)[1]
                x_plus_w = ev.instance_detections2D.get(key)[2]
                y_plus_h = ev.instance_detections2D.get(key)[3]
                image = frame[y:y_plus_h, x: x_plus_w]
                cv2.imwrite('data/' + obj['objectType'] + '/' + obj['objectType'] +
                            str(np.random.randint(1, 1000000)) + '.jpg', image)
    Yolo.yolo('image.jpg')


def get_object_type():
    file = open('Object Type.txt', 'r', 1)
    lines = file.buffer
    types = []
    for string in lines:
        string = string.rstrip()
        string = string.decode('utf-8')
        types.append(string)
    return types


def create_folder(types):
    for string in types:
        newpath = 'data/' + string
        if not os.path.exists(newpath):
            os.makedirs(newpath)


controller = ai2thor.controller.Controller()
controller.start()

# Kitchens: FloorPlan1 - FloorPlan30
# Living rooms: FloorPlan201 - FloorPlan230
# Bedrooms: FloorPlan301 - FloorPlan330
# Bathrooms: FloorPLan401 - FloorPlan430

controller.reset('FloorPlan1')
eve = controller.step(dict(action='Initialize', gridSize=0.1, renderObjectImage=True))
with keyboard.Listener(
        on_press=on_press, on_release=on_release) as listener:
    listener.join()
