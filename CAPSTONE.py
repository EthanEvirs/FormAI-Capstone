import cv2
import numpy

import mediapipe as mp
from mediapipe.tasks import python


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cam = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:

    while True:
        ret, frame = cam.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False

        results = pose.process(frame)
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        #Circle Color
        mp_drawing.DrawingSpec(color=(124,125,123), thickness = 2, circle_radius=4),
        #Line Color
        mp_drawing.DrawingSpec(color=(234,45,46), thickness = 2))



        #removes GUI from screen
        cv2.namedWindow('Camera', flags=cv2.WINDOW_GUI_NORMAL)
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()