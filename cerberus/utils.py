import cv2
import time


class Capture:
	"""
	Capture from cam class.
	"""
	def __init__(self, src=0, *args, **kwargs):
		self.src = src
		
	def start(self):
		print("[INFO] Starting video stream")
		self.cap = cv2.VideoCapture(self.src)
		self.run()
		
	def run(self):
		while True:
			ret, frame = self.cap.read()
			
			cv2.imshow("Frame", frame)
			
			if cv2.waitKey(20) & 0xFF == ord("q"):
				# press q to exit
				self.stop()
	
	def stop(self):
		print("[INFO] Stopping video stream")
		self.cap.release()
		cv2.destroyAllWindows()
