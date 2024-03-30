import cv2
import numpy as np

def nothing(x):
    pass

kernel = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
camera = cv2.VideoCapture(0)
if camera.isOpened():
    verdict, frame = camera.read()
    cv2.namedWindow('SpacialImage')
    cv2.createTrackbar('UpperThreshold', 'SpacialImage', 0, 50, nothing)
    cv2.createTrackbar('LowerThreshold', 'SpacialImage', 0, 50, nothing)
    if verdict:
        while (True):
            _, frame = camera.read()
            PIX_ON_THRESH = cv2.getTrackbarPos('UpperThreshold', 'SpacialImage')
            PIX_OFF_THRESH = (-1*cv2.getTrackbarPos('LowerThreshold', 'SpacialImage'))
            #need to subtract images and determine difference in pixel values
            diffFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype('int16')
            newFrame = cv2.filter2D(diffFrame,-1,kernel)
            #do the thresholding
            newFrame[np.where(newFrame<(PIX_OFF_THRESH))] = -127
            newFrame[np.where(newFrame >(PIX_ON_THRESH))] = 128
            newFrame += 127
            cv2.imshow('SpacialImage', newFrame.astype('uint8'))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
#make the dynamic ranges change with the number of events coming in