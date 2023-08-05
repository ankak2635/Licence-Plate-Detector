import easyocr
import string
# Initiate the OCR reader
reader = easyocr.Reader(['en'], gpu=True)

def get_car(licence_plate, vehicle_track_ids):
    '''
    A function to which assigns a id to the vehicles with detected licence plate
    '''
    x1,y1,x2,y2,score_plate,class_id = licence_plate

    got_car = False
    for i in range(len(vehicle_track_ids)):
        x1car, y1car, x2car, y2car, vehicle_id = vehicle_track_ids[i]
        car_index = i

        if x1>x1car and y1>y1car and x2<x2car and y2<y2car:
            got_car = True
            break

    if got_car:
        return vehicle_track_ids[car_index]
        
    return -1,-1,-1,-1,-1

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5',
                    'B':'8'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S',
                    '8': 'B'}

def format_complaince(text):
    '''
    Check if the licence plate complies with the required format.
    The format: XY12 ABC
    '''
    if len(text)!=7:
        return False
    
    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
       (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
       (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
       (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
       (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()) and \
       (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys()):
        return True
    else:
        return False
    
    
def format_licence_plate(text):
    '''
    Format text by mapping characters to mapping dict
    '''
    licence_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char,
               2: dict_char_to_int, 3: dict_char_to_int}

    for i in [0, 1, 2, 3, 4, 5, 6]:
        if text[i] in mapping[i].keys():
            licence_plate_ += mapping[i][text[i]]
        else:
            licence_plate_ += text[i]

    return licence_plate_



def read_licence_plate(licence_plate_crop):
    '''
    Read text from a given cropped licence plate image
    '''
    detections = reader.readtext(licence_plate_crop)

    for detection in detections:
        bbox, text, score = detection 

        text = text.upper().replace(' ', '')

        if format_complaince(text):
            return format_licence_plate(text=text), score
        
    return None, None
    

def write_csv(results, output_path):
    '''
    A function to write the results in desired csv format
    '''
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_no', 'vehicle_id', 'car_bbox',
                                                'licence_plate_bbox', 'licence_plate_bbox_score', 'licence_number',
                                                'licence_number_score'))

        for frame_no in results.keys():
            for vehicle_id in results[frame_no].keys():
                print(results[frame_no][vehicle_id])
                if 'car' in results[frame_no][vehicle_id].keys() and \
                   'licence_plate' in results[frame_no][vehicle_id].keys() and \
                   'text' in results[frame_no][vehicle_id]['licence_plate'].keys():
                    f.write('{},{},{},{},{},{},{}\n'.format(frame_no,
                                                            vehicle_id,
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_no][vehicle_id]['car']['bbox'][0],
                                                                results[frame_no][vehicle_id]['car']['bbox'][1],
                                                                results[frame_no][vehicle_id]['car']['bbox'][2],
                                                                results[frame_no][vehicle_id]['car']['bbox'][3]),
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_no][vehicle_id]['licence_plate']['bbox'][0],
                                                                results[frame_no][vehicle_id]['licence_plate']['bbox'][1],
                                                                results[frame_no][vehicle_id]['licence_plate']['bbox'][2],
                                                                results[frame_no][vehicle_id]['licence_plate']['bbox'][3]),
                                                            results[frame_no][vehicle_id]['licence_plate']['bbox_score'],
                                                            results[frame_no][vehicle_id]['licence_plate']['text'],
                                                            results[frame_no][vehicle_id]['licence_plate']['text_score'])
                            )
        f.close()

