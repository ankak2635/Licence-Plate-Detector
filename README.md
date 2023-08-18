# Vehicle License Plate Detection and Recognition System

This project focuses on identifying and extracting license plates from vehicles within a video stream. By leveraging YOLOv8, cv2, and easyOCR libraries.

## Libraries Used
The key libraries incorporated in this project are:
- YOLOv8: Utilized for object detection, particularly in identifying vehicles.
- cv2 (OpenCV): Employed for video manipulation and processing.
- easyOCR: Applied for accurate optical character recognition of license plates.

## Input and Output
🔗The input and output video files can be accessed [here](https://drive.google.com/drive/folders/1D8fKekW4e9xiA7sTP1nNq6igJivNePAn).

## Workflow
The project operates through the following steps:

1. **Vehicle Detection using YOLOv8**: The YOLOv8 model is deployed to identify cars within the video frames.

2. **Vehicle Tracking with SORT**: The Sort algorithm by [Alex Bewley](https://github.com/abewley/sort) is implemented to track vehicles as they move across frames.

3. **License Plate Detection**: A custom license plate detector, trained on a specialized dataset, is employed to locate license plates on vehicles.

4. **License Plate Processing**: Detected license plates are cropped and preprocessed for optimal recognition via easyOCR.

5. **License Plate Recognition**: easyOCR accurately recognizes characters on the license plates.

6. **Results Storage**: Extracted license plate information is structured and stored in a dataframe.

7. **Interpolation for Smoothness**: To ensure seamless video output, the dataframe is interpolated to fill in gaps in frames.

8. **Generating Video Output**: The processed dataframe is utilized to generate a video with bounding boxes encompassing vehicles and corresponding license plate text.

## Limitations
As of now, this project is specifically calibrated to read license plates conforming to the UK format: XY 12 ABC.

👏 The project is inspired by [computervisioneng](https://github.com/computervisioneng)—a big thanks for such fantastic computer vision tutorials.

