import cv2
import numpy as np

def nothing(x):
    pass

kernel = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
camera = cv2.VideoCapture(0)
spacial = 0
if camera.isOpened():
    verdict, frame1 = camera.read()
    cv2.namedWindow('SpacialImage')
    cv2.createTrackbar('UpperThreshold', 'SpacialImage', 0, 50, nothing)
    cv2.createTrackbar('LowerThreshold', 'SpacialImage', 0, 50, nothing)
    cv2.createTrackbar('Spacial', 'SpacialImage', 0, 1, nothing)
    PIX_ON_THRESH = 0
    PIX_OFF_THRESH = 0
    if verdict:
        while (True):
            _, frame2 = camera.read()
            spacial = cv2.getTrackbarPos('Spacial', 'SpacialImage')
            #PIX_ON_THRESH = cv2.getTrackbarPos('UpperThreshold', 'SpacialImage')
            #PIX_OFF_THRESH = (-1*cv2.getTrackbarPos('LowerThreshold', 'SpacialImage'))
            #determine if this is spacial or temporal
            if spacial:
                #need to subtract images and determine difference in pixel values
                diffFrame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY).astype('int16')
                newFrame = cv2.filter2D(diffFrame,-1,kernel)
                #do the thresholding
                newFrame[np.where(newFrame<(PIX_OFF_THRESH))] = -127
                newFrame[np.where(newFrame >(PIX_ON_THRESH))] = 128
                diffChange = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY).astype('int') - cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY).astype('int')
                negative = np.sum(diffChange < (PIX_OFF_THRESH))
                positive = np.sum(diffChange > (PIX_ON_THRESH))
                print(str(positive) + " " + str(negative))
                if (positive > 10000):
                    PIX_ON_THRESH+=1
                if (negative > 10000):
                    PIX_OFF_THRESH-=1
                newFrame += 127
                cv2.imshow('SpacialImage', newFrame.astype('uint8'))
            else:
                diffFrame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY).astype('int') - cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY).astype('int')
                # do the thresholding
                diffFrame[np.where(diffFrame < (PIX_OFF_THRESH))] = -127
                diffFrame[np.where(diffFrame > (PIX_ON_THRESH))] = 128
                diffFrame += 127
                cv2.imshow('SpacialImage', diffFrame.astype('uint8'))
                # get new frame1
                frame1 = frame2
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # get new frame1
            frame1 = frame2
#make the dynamic ranges change with the number of events coming in