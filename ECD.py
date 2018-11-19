#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
from Extract import *
from Convert import *
from Display import *

# filename of clip to load
filename = 'clip.mp4'
lock = threading.Lock()
# shared queue  
extractionQueue = queue.Queue(10)
sendingQueue = queue.Queue(10)
flagQueue = queue.Queue(2); flagQueue.put(True); flagQueue.put(True);


threadExtraction = Extract(filename,extractionQueue, lock, flagQueue)
threadExtraction.start()
threadConvert = Convert(extractionQueue, sendingQueue, lock, flagQueue)
threadConvert.start()
threadDisplay = Display(sendingQueue, flagQueue)
threadDisplay.start()

