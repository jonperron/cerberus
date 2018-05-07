#! /usr/bin/python3

import cv2
import time

class FirstHead:
    """
    First Head : Watching.
	
    Interact with webcam to record images.
    """
    def __init__(
        self,
        frame_interval=5000,
        src=0,
        *args,
        **kwargs
    ):
        """
        :param frame_interval: Interval between two frames, in ms.
        :type frame_interval: int.
        :param src: Webcam source.
        :type src: int.
        """
        self.src = src
        self.frame_interval = frame_interval
        self.capture = None

    def start(self):
        if not self.capture:
            print("[INFO] Starting video stream")
            self.capture = cv2.VideoCapture(self.src)
        return self.capture
	
    def stop(self):
        print("[INFO] Stopping video stream")
        self.capture.release()
        cv2.destroyAllWindows()
		
		
