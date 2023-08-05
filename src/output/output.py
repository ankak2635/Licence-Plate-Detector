import ast
import cv2
import numpy as np
import pandas as pd

def draw_border(img,top_left, bottom_right, color=(0,255,0), thickness = 10, line_length_x = 200, line_length_y = 200):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv2.line(img, (x1, y1), (x1, y1 + line_length_y), color, thickness)  #-- top-left
    cv2.line(img, (x1, y1), (x1 + line_length_x, y1), color, thickness)

    cv2.line(img, (x1, y2), (x1, y2 - line_length_y), color, thickness)  #-- bottom-left
    cv2.line(img, (x1, y2), (x1 + line_length_x, y2), color, thickness)

    cv2.line(img, (x2, y1), (x2 - line_length_x, y1), color, thickness)  #-- top-right
    cv2.line(img, (x2, y1), (x2, y1 + line_length_y), color, thickness)

    cv2.line(img, (x2, y2), (x2, y2 - line_length_y), color, thickness)  #-- bottom-right
    cv2.line(img, (x2, y2), (x2 - line_length_x, y2), color, thickness)

    return img

# read interpolated data
results = pd.read_csv('./test_interpolated.csv')

# load video
video_path = './sample.mp4'
cap = cv2.VideoCapture(video_path)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('./final_out.mp4', fourcc, fps, (width, height))

licence_plate = {}
for vehicle_id in np.unique(results['vehicle_id']):
    max_ = np.amax(results[results['vehicle_id'] == vehicle_id]['licence_number_score'])
    licence_plate[vehicle_id] = {'licence_crop': None,
                             'licence_plate_number': results[(results['vehicle_id'] == vehicle_id) &
                                                             (results['licence_number_score'] == max_)]['licence_number'].iloc[0]}
    cap.set(cv2.CAP_PROP_POS_FRAMES, results[(results['vehicle_id'] == vehicle_id) &
                                             (results['licence_number_score'] == max_)]['frame_no'].iloc[0])
    ret, frame = cap.read()

    x1, y1, x2, y2 = ast.literal_eval(results[(results['vehicle_id'] == vehicle_id) &
                                              (results['licence_number_score'] == max_)]['licence_plate_bbox'].iloc[0].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))

    licence_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
    licence_crop = cv2.resize(licence_crop, (int((x2 - x1) * 400 / (y2 - y1)), 400))

    licence_plate[vehicle_id]['licence_crop'] = licence_crop


frame_no = -1

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# read frames
ret = True
while ret:
    ret, frame = cap.read()
    frame_no += 1
    if ret:
        df_ = results[results['frame_no'] == frame_no]
        for row_indx in range(len(df_)):
            # draw car
            car_x1, car_y1, car_x2, car_y2 = ast.literal_eval(df_.iloc[row_indx]['car_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))
            draw_border(frame, (int(car_x1), int(car_y1)), (int(car_x2), int(car_y2)), (0, 255, 0), 25,
                        line_length_x=200, line_length_y=200)

            # draw licence plate
            x1, y1, x2, y2 = ast.literal_eval(df_.iloc[row_indx]['licence_plate_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 12)

            # crop licence plate
            licence_crop = licence_plate[df_.iloc[row_indx]['vehicle_id']]['licence_crop']

            H, W, _ = licence_crop.shape

            try:
                frame[int(car_y1) - H - 100:int(car_y1) - 100,
                      int((car_x2 + car_x1 - W) / 2):int((car_x2 + car_x1 + W) / 2), :] = licence_crop

                frame[int(car_y1) - H - 400:int(car_y1) - H - 100,
                      int((car_x2 + car_x1 - W) / 2):int((car_x2 + car_x1 + W) / 2), :] = (255, 255, 255)

                (text_width, text_height), _ = cv2.getTextSize(
                    licence_plate[df_.iloc[row_indx]['vehicle_id']]['licence_plate_number'],
                    cv2.FONT_HERSHEY_SIMPLEX,
                    4.3,
                    17)

                cv2.putText(frame,
                            licence_plate[df_.iloc[row_indx]['vehicle_id']]['licence_plate_number'],
                            (int((car_x2 + car_x1 - text_width) / 2), int(car_y1 - H - 250 + (text_height / 2))),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            4.3,
                            (0, 0, 0),
                            17)

            except:
                pass

        out.write(frame)
        frame = cv2.resize(frame, (1280, 720))

        # cv2.imshow('frame', frame)
        # cv2.waitKey(0)

out.release()
cap.release()

