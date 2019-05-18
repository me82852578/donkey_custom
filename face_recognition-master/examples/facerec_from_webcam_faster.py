import face_recognition
import cv2
import numpy as np
from imutils.video import VideoStream
import time
import argparse


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoCapture(0)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
args = vars(ap.parse_args())

# Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoStream(src=0)
video_capture= VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a second sample picture and learn how to recognize it.
august_image = face_recognition.load_image_file("august.jpg")
august_face_encoding = face_recognition.face_encodings(august_image)[0]

# Load a second sample picture and learn how to recognize it.
jerry_image = face_recognition.load_image_file("jerry.jpg")
jerry_face_encoding = face_recognition.face_encodings(jerry_image)[0]

jay_image = face_recognition.load_image_file("jay.jpg")
jay_face_encoding = face_recognition.face_encodings(jay_image)[0]

andrew_image = face_recognition.load_image_file("andrew.jpg")
andrew_face_encoding = face_recognition.face_encodings(andrew_image)[0]

angel_image = face_recognition.load_image_file("angel.jpg")
angel_face_encoding = face_recognition.face_encodings(angel_image)[0]

chi_image = face_recognition.load_image_file("chi.jpg")
chi_face_encoding = face_recognition.face_encodings(chi_image)[0]

hym_image = face_recognition.load_image_file("hym.jpg")
hym_face_encoding = face_recognition.face_encodings(hym_image)[0]

shao_image = face_recognition.load_image_file("shao.jpg")
shao_face_encoding = face_recognition.face_encodings(shao_image)[0]

tze_image = face_recognition.load_image_file("tze.jpg")
tze_face_encoding = face_recognition.face_encodings(tze_image)[0]

wei_image = face_recognition.load_image_file("wei.jpg")
wei_face_encoding = face_recognition.face_encodings(wei_image)[0]

yang_image = face_recognition.load_image_file("yang.jpg")
yang_face_encoding = face_recognition.face_encodings(yang_image)[0]

ginger_image = face_recognition.load_image_file("ginger.jpg")
ginger_face_encoding = face_recognition.face_encodings(ginger_image)[0]

tintin_image = face_recognition.load_image_file("tintin.jpg")
tintin_face_encoding = face_recognition.face_encodings(tintin_image)[0]

yi_image = face_recognition.load_image_file("yi.jpg")
yi_face_encoding = face_recognition.face_encodings(yi_image)[0]

kei_image = face_recognition.load_image_file("kei.jpg")
kei_face_encoding = face_recognition.face_encodings(kei_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    august_face_encoding,
    jerry_face_encoding,
    jay_face_encoding,
    andrew_face_encoding,
    angel_face_encoding,
    chi_face_encoding,
    hym_face_encoding,
    shao_face_encoding,
    tze_face_encoding,
    wei_face_encoding,
    yang_face_encoding,
    ginger_face_encoding ,
    tintin_face_encoding,
    yi_face_encoding ,
    kei_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "August Lu",
    "Jerry Ke",
    "Jay",
    "Andrew",
    "Angel",
    "Chi",
    "HYM",
    "Shao",
    "Tze",
    "Wei",
    "Yang",
    "Ginger",
    "TinTin",
    "Yi",
    "Kei"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    # ret, frame = video_capture.read()
    frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
