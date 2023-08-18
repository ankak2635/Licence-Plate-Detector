# Licence Plate Detector

This project **detects and reads licence plates** of vehicles from a video.

The project utilizes YOLOv8, OpenCV and easyOCR as the major libraries.

🔗 The input and output videos can be found [here](https://drive.google.com/drive/folders/1D8fKekW4e9xiA7sTP1nNq6igJivNePAn?usp=sharing).

YOLOv8's pre-trained coco-model is used to detect cars and a licence plate detector is trained on a custom dataset. [Sort](https://github.com/abewley/sort) by Alex Bewley is used to track vehicles. The cv2 library has been utilized for video manipulation.

Steps:
* Yolo model detects car.
* Sort module tracks the car through the video.
* Licence plate detector detects the plates; assigns the plate to the cars
* Crops and processes the licence plate before reading it via EasyOCR.
* Writes the results as a dataframe.
* Interplolates the dataframe to fill in the missing frames to obtain smooth video output. 
* Utilizes the dataframe to generate the video output with bounding boxes and licence plate  text.


Limitations:
So far this project has been formatted to read the UK licence plates which have the following format: XY 12 ABC. 

The project is inspired by [computervisioneng](https://github.com/computervisioneng)—a big thanks for such fantastic computer vision tutorials. 
