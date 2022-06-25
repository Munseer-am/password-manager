import cv2
import datetime
import os
import time

x = str(datetime.datetime.now())
x.replace(":", "-")


def capture(log_dir):
	cam = cv2.VideoCapture(0)
	result, img = cam.read()
	time.sleep(0.5)
	cv2.imwrite(os.path.join(log_dir, f"{x}.jpg"), img)
	cam.release()
	cv2.destroyAllWindows()