import cv2
import numpy as np
import dlib
import math
import pyglet
import time
import pygame

def start():
    cap = cv2.VideoCapture(0)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    font = cv2.FONT_HERSHEY_SIMPLEX
    counter = 0
    # sound = pyglet.media.load("beep.wav", streaming=False)
    pygame.mixer.init()  
    # pygame.mixer.music.load("beep.wav")
    # pygame.mixer.music.queue("truck_horn.wav")


    def midpoint(p1, p2):
        return (int)((p1.x + p2.x)/2), (int)((p1.y + p2.y)/2)

    def get_blinking_ratio(eye_points, facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
        hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
        ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)
        hor_line_length = math.hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_length = math.hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
        ratio = hor_line_length / ver_line_length
        return ratio


    while(True):
        if counter == 0:
            pygame.mixer.music.pause()
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret is False:
            break
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.putText(frame, "Counter: " + str(counter), (50, 50), font, 2, (255, 255, 255))
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            eye_aspect_ratio = (left_eye_ratio + right_eye_ratio) / 2
            if eye_aspect_ratio > 3:
                cv2.putText(frame, "CLOSED", (0, 400), font, 2, (0, 0, 255))
                counter+=1
            else:
                counter = 0


        if counter>25:
            pygame.mixer.music.load("beep.wav")
            pygame.mixer.music.play()
        
        if counter > 40:
            pygame.mixer.music.load("focus.wav")
            pygame.mixer.music.play()

        


        # # Smooths images out
        # gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # rows, cols = gray.shape
        # # Setting display of only above a certain threshold of colour (isolate blacks)
        # _, threshold = cv2.threshold(gray, 3, 255, cv2.THRESH_BINARY_INV)

        # # Find contours of edges and print them in image
        # contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        # for cnt in contours:
        #     (x, y, w, h) = cv2.boundingRect(cnt)
        #     cv2.drawContours(gray, [cnt], -1, (0, 0, 255), 3)

        #     # Blue rectangle of size of screen tracking the pupil
        #     cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

        #     # Green cross in centre of rectangle
        #     cv2.line(gray, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
        #     cv2.line(gray, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)
        #     break
        



        # Display the resulting frame

        # Grayscale threshold only
        # cv2.imshow("Threshold", threshold)

        # Gray face only
        cv2.imshow('Webcam',frame) 

        # Press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
