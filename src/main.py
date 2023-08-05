from ultralytics import YOLO
import pandas as pd
import numpy as np
import cv2
from sort_module.sort import *
from src.utils import get_car, read_licence_plate, write_csv


# load models
vehicle_detector = YOLO('yolov8n.pt')
plate_detector =  YOLO('./models/license_plate_detector.pt')
vehicle_tracker = Sort()

results = {}

# load video
cap = cv2.VideoCapture('./sample.mp4')

# define vehiles class
vehicles= [2,3,5,7] # as of coco object class id

# read frames
frame_no= -1
ret=True

while ret:
    frame_no += 1
    ret, frame = cap.read()
    results[frame_no]= {}

    # detect vehicles
    detections = vehicle_detector(frame)[0]
    detections_ =[]
    
    for detection in detections.boxes.data.tolist():
        x1,y1,x2,y2,score,class_id = detection
        if int(class_id) in vehicles:
            detections_.append([x1,y1,x2,y2,score])

    # track vehicles
    track_ids = vehicle_tracker.update(np.asarray(detections_))
    

    # detect licence plate
    licence_plates = plate_detector(frame)[0]
    for licence_plate in licence_plates.boxes.data.tolist():
        x1,y1,x2,y2,score_plate,class_id = licence_plate

        # assign licence plate to car
        x1car, y1car, x2car, y2car, vehicle_id = get_car(licence_plate, track_ids)

        # if vehicle_id != -1:
        # crop licence plate
        plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

        # process licence plate
        plate_crop_grey = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2GRAY)
        _, plate_crop_thres = cv2.threshold(plate_crop_grey, 64, 255, cv2.THRESH_BINARY_INV)


        # read licence plate
        licence_plate_text, licence_plate_score = read_licence_plate(plate_crop_thres)
        
        if licence_plate_text is not None:
            results[frame_no][vehicle_id] = {'car': {'bbox': [x1car, y1car, x2car, y2car]},
                                            'licence_plate': {'bbox': [x1, y1, x2, y2],
                                                                'text': licence_plate_text,
                                                                'bbox_score': score_plate,
                                                                'text_score': licence_plate_score}}
# write results
write_csv(results, './test.csv')


