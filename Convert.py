import threading
import cv2
import numpy as np
import base64
import queue
import time
class Convert(threading.Thread):
    inputBuff = None
    outputBuff = None
    flagQueue = None
    def __init__ (self, inputBuff, outputBuff,lock, flagQueue):
        threading.Thread.__init__(self)
        Convert.inputBuff = inputBuff
        Convert.outputBuff = outputBuff
        Convert.flagQueue = flagQueue
        self.lock = lock

    def run(self):
        count = 0
        while Convert.flagQueue.qsize() == 2:
            if not Convert.inputBuff.empty():
                #self.lock.acquire()
                while Convert.inputBuff.empty():
                    #self.lock.release()
                    time.sleep(.300)
                    #self.lock.acquire()

                frameAsText = Convert.inputBuff.get()
                #self.lock.release()
                # decode the frame 
                jpgRawImage = base64.b64decode(frameAsText)

                # convert the raw frame to a numpy array
                jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        
                # get a jpg encoded frame
                img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

                grayscaleFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                print("converting to grayscale frame: {}".format(count))   

                success, jpgImage = cv2.imencode('.jpg', grayscaleFrame)
    
                #encode the frame as base 64 to make debugging easier
                jpgAsText = base64.b64encode(jpgImage)
                #self.lock.acquire()
                # add the frame to the buffer
                Convert.outputBuff.put(jpgAsText)
                while (Convert.outputBuff.full()):
                    time.sleep(0.000002)  
                #self.lock.release()
                count += 1
        Convert.flagQueue.get()