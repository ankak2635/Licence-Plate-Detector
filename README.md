This project **detects licence plates** of vehicles from a video.

The project utilizes YOLOv8, cv2 and easyOCR as the major libraries.

YOLOv8's pre-trained coco-model is used to detect cars and a licence plate detector is trained on custom dataset. Sortby Alex Bewley is used to track vehicles. cv2 has been utilized for video manipulation.

The input and output videos can be found here .

Steps:
* Yolo model detects car.
* Sort module tracks the car through the video.
* Licence plate detector detects the plates; assign the plate to the cars
* Crops and processes the licence plate before reading it via EasyOCR.
* Writes the results as a dataframe.
* Interplolates the dataframe to fill in the missing frames to obtain smooth video output. 
* Utilizes the dataframe to generate the video output with bounding boxes and licence plate  text.


Limitations:
So far this projects has been formatted to read the UK licence plates which has the following format: XY 12 ABC. 


