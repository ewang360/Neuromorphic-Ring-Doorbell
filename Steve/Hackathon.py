import cv2
import numpy as np

def nothing(x):
    pass

#config
noiseReductionValueSpacial = 50

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
                newFrame += 127
                #use median blur to reduce background effects
                diffMedianImage = cv2.medianBlur(diffFrame,3)
                #get difference image
                noiseImage = diffFrame - diffMedianImage
                #determine the number of noise parts in image
                negative = np.sum(noiseImage < (PIX_OFF_THRESH))
                positive = np.sum(noiseImage > (PIX_ON_THRESH))
                if (positive > noiseReductionValueSpacial):
                    PIX_ON_THRESH+=2
                if (negative > noiseReductionValueSpacial):
                    PIX_OFF_THRESH-=2
                cv2.imshow('SpacialImage', newFrame.astype('uint8'))
            else:
                diffFrame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY).astype('int16') - cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY).astype('int16')
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