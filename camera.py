import cv2

class Camera():
    def __init__(self):
        self.cam = cv2.VideoCapture(0)

        if not self.cam.isOpened():
            raise Exception("Could not open Camera")

        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def start_capture(self):
        while True:
            ret, frame = self.cam.read()
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) == ord('q'):
                break

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()