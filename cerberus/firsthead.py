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

	def start(self):
		print("[INFO] Starting video stream")
		self.capture = cv2.VideoCapture(self.src)
		self.run()
		
	def run(self):
		while True:
			ret, frame = self.capture.read()
            
            return frame
	
	def stop(self):
		print("[INFO] Stopping video stream")
		self.cap.release()
		cv2.destroyAllWindows()
		
		
