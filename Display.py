import threading
import cv2
import numpy as np
import base64
import queue
import time
class Display(threading.Thread):
    flagQueue = False
    inputBuff = None
    def __init__ (self, inputBuff, flagQueue):
        threading.Thread.__init__(self)
        Display.inputBuff = inputBuff
        Display.flagQueue = flagQueue

    def run(self):
        count = 0
        # go through each frame in the buffer until the buffer is empty
        while not Display.flagQueue.empty():
            if not Display.inputBuff.empty():
                # get the next frame
                frameAsText = Display.inputBuff.get()

                # decode the frame 
                jpgRawImage = base64.b64decode(frameAsText)

                # convert the raw frame to a numpy array
                jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        
                # get a jpg encoded frame
                img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

                print("Displaying frame {}".format(count))        

                # display the image in a window called "video" and wait 42ms
                # before displaying the next frame
                cv2.imshow("Video", img)
                if cv2.waitKey(42) and 0xFF == ord("q"):
                    break

                count += 1

        print("Finished displaying all frames")
        # cleanup the windows
        cv2.destroyAllWindows()