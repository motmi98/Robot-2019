# Robotics

Object dection using YOLOv3, OpenCV and robot trajectory  in a virtual environment Ai2thor

## Getting Started

Get this project using 
```
git clone: https://github.com/pxthanh98/robotics.git
```
### Requirements
System
  *  OS: Mac OS X 10.9+, Ubuntu 14.04+
  *  Graphics Card: DX9 (shader model 3.0) or DX11 with feature level 9.3 capabilities.
  *  CPU: SSE2 instruction set support.
  *  Python 3.5+
  *  Linux: X server with GLX module enabled


pip requirements:
```
ai2thor
keyboard
numpy
matplotlib
opencv
pillow
pynout
numpy
```

### Installing

Ai2thor
```
pip install ai2thor
```
OpenCV
```
pip install opencv
```
Matplotlib
```
pip install matplotlib
```
Pynput
```
pip install pynput
```
Keyboard
```
pip install keyboard
```

### Compiling
1) For object decection:
* Step 1
Download the weights file into folder 'challenge 1' and unzip it
```
https://drive.google.com/file/d/1nks4PxeFBiiSZP-KQCi9U0WPRt_Gk6Ut/view?usp=sharing
```
* Step 2
```
cd 'challenge 1'
python main.py
```
* Step 3
```
Using keyboard for navigation in ai2thor
 'w': Move ahead
 's': Move back
 'a': Move to the left
 'd': Move to the right
 'h': Turn left 90 degree
 'l': Turn right 90 degree
 'j': Look down 30 degree
 'k': Look up 30 degree
 'esc': Escape
```
* Step 4
Press 'c' to get an image and prediction. Preidction will be written to the image```prediction.jpg```

2) For trajectory:
* Step 1
```
cd 'challenge 2'
sudo python trajectory.py
```
* Step 2
```
Using keyboard for navigation in ai2thor
'up arrow': Move ahead
'down arrow': Move back
'left arrow': Move to the left
'right arrow': Move to the right
'h': Turn left 90 degree
'l': Turn right 90 degree
'j': Look down 30 degree
'k': Look up 30 degree
'esc': Escape
```
## Acknowledgments

* https://towardsdatascience.com/yolo-object-detection-with-opencv-and-python-21e50ac599e9
* https://github.com/allenai/ai2thor/issues/124


