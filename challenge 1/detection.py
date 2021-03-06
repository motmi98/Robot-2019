import cv2
import numpy as np
import os

my_file = open("yolo_weights/thor.names", "r")
thor_names = [line.strip() for line in my_file]

colors = np.random.uniform(0, 255, size=(len(thor_names), 3))
confidences = []
bounds = []
ids = []
conf_threshold = 0.5
nms_threshold = 0.4

def get_output_layer(dnn):
	name = dnn.getLayerNames()
	output = [name[i[0]-1] for i in dnn.getUnconnectedOutLayers()]
	return output

def draw(image, id, conf, x, y, w, h):
    label = str(thor_names[id])
    color = colors[id]
    cv2.rectangle(image, (x,y), (w,h), color)
    cv2.putText(image, label + " " + str(round(100*conf)) + "%", (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def non_max_suppression(image, bound, confidence, conf_threshold, nms_threshold):
	indices = cv2.dnn.NMSBoxes(bound, confidence, conf_threshold, nms_threshold)
	for i in indices:
		i = i[0]
		box = bound[i]
		x = box[0]
		y = box[1]
		w = box[2]
		h = box[3]
		draw(image, ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

def detect(object_name):
	image = cv2.imread(object_name)
	height = image.shape[0]
	width = image.shape[1]
	channels = image.shape[2]

	dnn = cv2.dnn.readNet('yolo_weights/yolov3-thor_final.weights', 'yolo_weights/yolov3-thor.cfg')
	processed_image = cv2.dnn.blobFromImage(image, 0.00392, (416,416), (0,0,0), True, crop=False) 
	dnn.setInput(processed_image)

	outputs = dnn.forward(get_output_layer(dnn))
	for results in outputs:
		for result in results:
			score = result[5:]
			id = np.argmax(score)
			confidence = score[id]
			if confidence > conf_threshold:
				w = int(result[2] * width)
				h = int(result[3] * height)
				x = int(result[0] * width) - w / 2
				y = int(result[1] * height) - h /2
				ids.append(id)
				confidences.append(float(confidence))
				bounds.append([x, y, w, h])

	non_max_suppression(image, bounds, confidences, conf_threshold, nms_threshold)
	if (os.path.exists('prediction.jpg')):
		os.remove('prediction.jpg')
		cv2.imwrite("prediction.jpg", image)
		print("Done.")
	else:
		cv2.imwrite("prediction.jpg", image)
		print("Done.")
