import csv
import numpy as np
from scipy.interpolate import interp1d


def interpolate_bounding_boxes(data):
    # Extract necessary data columns from input data
    frame_numbers = np.array([int(row['frame_no']) for row in data])
    vehicle_ids = np.array([int(float(row['vehicle_id'])) for row in data])
    car_bboxes = np.array([list(map(float, row['car_bbox'][1:-1].split())) for row in data])
    licence_plate_bboxes = np.array([list(map(float, row['licence_plate_bbox'][1:-1].split())) for row in data])

    interpolated_data = []
    unique_vehicle_ids = np.unique(vehicle_ids)
    for vehicle_id in unique_vehicle_ids:

        frame_numbers_ = [p['frame_no'] for p in data if int(float(p['vehicle_id'])) == int(float(vehicle_id))]
        print(frame_numbers_, vehicle_id)

        # Filter data for a specific car ID
        car_mask = vehicle_ids == vehicle_id
        car_frame_numbers = frame_numbers[car_mask]
        car_bboxes_interpolated = []
        licence_plate_bboxes_interpolated = []

        first_frame_number = car_frame_numbers[0]
        last_frame_number = car_frame_numbers[-1]

        for i in range(len(car_bboxes[car_mask])):
            frame_number = car_frame_numbers[i]
            car_bbox = car_bboxes[car_mask][i]
            licence_plate_bbox = licence_plate_bboxes[car_mask][i]

            if i > 0:
                prev_frame_number = car_frame_numbers[i-1]
                prev_car_bbox = car_bboxes_interpolated[-1]
                prev_licence_plate_bbox = licence_plate_bboxes_interpolated[-1]

                if frame_number - prev_frame_number > 1:
                    # Interpolate missing frames' bounding boxes
                    frames_gap = frame_number - prev_frame_number
                    x = np.array([prev_frame_number, frame_number])
                    x_new = np.linspace(prev_frame_number, frame_number, num=frames_gap, endpoint=False)
                    interp_func = interp1d(x, np.vstack((prev_car_bbox, car_bbox)), axis=0, kind='linear')
                    interpolated_car_bboxes = interp_func(x_new)
                    interp_func = interp1d(x, np.vstack((prev_licence_plate_bbox, licence_plate_bbox)), axis=0, kind='linear')
                    interpolated_licence_plate_bboxes = interp_func(x_new)

                    car_bboxes_interpolated.extend(interpolated_car_bboxes[1:])
                    licence_plate_bboxes_interpolated.extend(interpolated_licence_plate_bboxes[1:])

            car_bboxes_interpolated.append(car_bbox)
            licence_plate_bboxes_interpolated.append(licence_plate_bbox)

        for i in range(len(car_bboxes_interpolated)):
            frame_number = first_frame_number + i
            row = {}
            row['frame_no'] = str(frame_number)
            row['vehicle_id'] = str(vehicle_id)
            row['car_bbox'] = ' '.join(map(str, car_bboxes_interpolated[i]))
            row['licence_plate_bbox'] = ' '.join(map(str, licence_plate_bboxes_interpolated[i]))

            if str(frame_number) not in frame_numbers_:
                # Imputed row, set the following fields to '0'
                row['licence_plate_bbox_score'] = '0'
                row['licence_number'] = '0'
                row['licence_number_score'] = '0'
            else:
                # Original row, retrieve values from the input data if available
                original_row = [p for p in data if int(p['frame_no']) == frame_number and int(float(p['vehicle_id'])) == int(float(vehicle_id))][0]
                row['licence_plate_bbox_score'] = original_row['licence_plate_bbox_score'] if 'licence_plate_bbox_score' in original_row else '0'
                row['licence_number'] = original_row['licence_number'] if 'licence_number' in original_row else '0'
                row['licence_number_score'] = original_row['licence_number_score'] if 'licence_number_score' in original_row else '0'

            interpolated_data.append(row)

    return interpolated_data


# Load the CSV file
with open('test.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Interpolate missing data
interpolated_data = interpolate_bounding_boxes(data)

# Write updated data to a new CSV file
header = ['frame_no', 'vehicle_id', 'car_bbox', 'licence_plate_bbox', 'licence_plate_bbox_score', 'licence_number', 'licence_number_score']
with open('test_interpolated.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerows(interpolated_data)