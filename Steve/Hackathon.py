import cv2
import numpy as np

def nothing(x):
    pass

#config
noiseReductionValueSpacial = 20

kernel = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
camera = cv2.VideoCapture(0)
spacial = 0
PIX_OFF_THRESH_TEMP = -25
PIX_ON_THRESH_TEMP = 25
PIX_ON_THRESH_SPACIAL = 0
PIX_OFF_THRESH_SPACIAL = 0
averageEvents = 0
influenceFactor = .9
if camera.isOpened():
    verdict, frame1 = camera.read()
    cv2.namedWindow('SpacialImage')
    cv2.namedWindow('TemporalImage')
    if verdict:
        while (True):
            _, frame2 = camera.read()
            #PIX_ON_THRESH = cv2.getTrackbarPos('UpperThreshold', 'SpacialImage')
            #PIX_OFF_THRESH = (-1*cv2.getTrackbarPos('LowerThreshold', 'SpacialImage'))
            #determine if this is spacial or temporal

            diffFrame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY).astype('int16') - cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY).astype('int16')
            # do the thresholding
            diffFrame[np.where(diffFrame < (PIX_OFF_THRESH_TEMP))] = -127
            diffFrame[np.where(diffFrame > (PIX_ON_THRESH_TEMP))] = 128
            currentEvents = np.sum(diffFrame < (PIX_OFF_THRESH_TEMP))
            currentEvents += np.sum(diffFrame > (PIX_ON_THRESH_TEMP))
            diffFrame += 127
            cv2.imshow('TemporalImage', diffFrame.astype('uint8'))
            averageEvents = (influenceFactor*averageEvents) + ((1-influenceFactor)*currentEvents)
            currentEvents = 0
            #print(str(averageEvents))
            #activate spacial
            if averageEvents > 15000:
                #need to subtract images and determine difference in pixel values
                diffFrameSpacial = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY).astype('int16')
                newFrame = cv2.filter2D(diffFrameSpacial,-1,kernel)
                #do the thresholding
                newFrame[np.where(newFrame<(PIX_OFF_THRESH_SPACIAL))] = -127
                newFrame[np.where(newFrame >(PIX_ON_THRESH_SPACIAL))] = 128
                newFrame += 127
                #use median blur to reduce background effects
                diffMedianImage = cv2.medianBlur(diffFrameSpacial,3)
                #get difference image
                noiseImage = diffFrameSpacial - diffMedianImage
                #determine the number of noise parts in image
                negative = np.sum(noiseImage < (PIX_OFF_THRESH_SPACIAL))
                positive = np.sum(noiseImage > (PIX_ON_THRESH_SPACIAL))
                if (positive > noiseReductionValueSpacial):
                    PIX_ON_THRESH_SPACIAL+=2
                else:
                    PIX_ON_THRESH_SPACIAL -= 2
                if (negative > noiseReductionValueSpacial):
                    PIX_OFF_THRESH_SPACIAL-=2
                else:
                    PIX_OFF_THRESH_SPACIAL += 2
                cv2.imshow('SpacialImage', newFrame.astype('uint8'))
            else:
                cv2.imshow('SpacialImage', (np.zeros((diffFrame.shape[0],diffFrame.shape[1]))+127).astype('uint8'))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # get new frame1
            frame1 = frame2