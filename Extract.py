import threading
import cv2
import numpy as np
import base64
import queue
import time
class Extract(threading.Thread):
    Outputbuff = None
    flagQueue= None
    def __init__(self,fileName,Outputbuff, lock, flagQueue):
        threading.Thread.__init__(self)
        self.fileName = fileName
        Extract.Outputbuff = Outputbuff# Initialize frame count 
        self.lock = lock
        Extract.flagQueue = flagQueue

    def run(self):
        count = 0

        # open video file
        vidcap = cv2.VideoCapture(self.fileName)

        # read first image
        success,image = vidcap.read()
    
        print("Reading frame {} {} ".format(count, success))
        while success:
            # get a jpg encoded frame
            success, jpgImage = cv2.imencode('.jpg', image)

            #encode the frame as base 64 to make debugging easier
            jpgAsText = base64.b64encode(jpgImage)


            #self.lock.acquire()
            Extract.Outputbuff.put(jpgAsText)
            # add the frame to the buffer
            while (Extract.Outputbuff.full()):
                time.sleep(0.02)
            #self.lock.release()

            success,image = vidcap.read()
            print('Reading frame {} {}'.format(count, success))
            count += 1

            print("Frame extraction complete")
        Extract.flagQueue.get()