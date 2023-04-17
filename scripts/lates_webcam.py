import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import yaml

import face_recognition
from scripts import time_manager, mysql_manager, face_registry, util, lates_logger

def start_webcam(lessonid: int):
    tolerance = 0.6
    inputsource = 0
    sensitivity = 3

    try:
        config = yaml.safe_load(open('./conf.yaml'))
        tolerance = float(config['tolerance'])
        inputsource = config['inputsource']
        sensitivity = int(config['sensitivity'])
        
    except Exception as e:
        print(f"[Config Error] {e}, using default tolerance level ({tolerance})")
        
    video_capture = cv2.VideoCapture(inputsource)

    mysql_manager.load_all(lessonid)

    detected_faces = []
    for student in face_registry.known_face_names:
        detected_faces.append((student, -1))

    detections_left = []
    for student in face_registry.known_face_names:
        detections_left.append((student, sensitivity))

    paused = False

    font = ImageFont.truetype("arial.ttf", size=25)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()

        image = Image.fromarray(frame)
        draw = ImageDraw.Draw(image)

        time = time_manager.get_time()
        draw.text((6, 6), ':'.join([str(i).rjust(2, '0') for i in time]), fill=(0, 0, 0, 255), font=font)

        if not paused:
            small_frame = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(
                rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(
                    face_registry.known_face_encodings, face_encoding, tolerance=tolerance)
                name = "Unknown"

                face_distances = face_recognition.face_distance(
                    face_registry.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = face_registry.known_face_names[best_match_index]

                    i = util.find_tuple(detections_left, 0, name)
                    if detections_left[i][1] > 0: detections_left[i] = (name, detections_left[i][1] - 1)
                    elif detections_left[i][1] == 0: 
                        detections_left[i] = (name, -1)
                        lates_logger.save(name, time_manager.get_latency(lessonid))

                face_names.append(name)

            for i in range(len(detections_left)):
                if not (detections_left[i][0] in face_names) and detections_left[i][1] != -1:
                    detections_left[i] = (detections_left[i][0], sensitivity)

            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 1.25
                right *= 1.25
                bottom *= 1.25
                left *= 1.25

                text_width, text_height = draw.textsize(name, font=font)

                draw.rectangle(((left, top), (right, bottom)),
                               outline=(0, 0, 255))
                draw.rectangle(((left, bottom - text_height - 10),
                               (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))

                draw.text((left + 6, bottom - text_height - 5),
                          name, fill=(255, 255, 255, 255), font=font)

        del draw

        cv2.imshow(
            f'Lates Webcam - {mysql_manager.get_lesson_name(lessonid)}', np.array(image))

        key = cv2.waitKey(1) & 0xFF

        if key == ord('p'):
            paused = not paused
            print(("Paused" if paused else "Resumed") + " face recognition!")
        if key == ord('q'):
            lates_logger.log()
            exit(0)
        if time_manager.is_end():
            break

    video_capture.release()
    cv2.destroyAllWindows()

    lates_logger.log()
