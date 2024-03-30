import cv2
import numpy as np

def nothing(x):
    pass

kernel = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
camera = cv2.VideoCapture(0)
spacial = 0
PIX_ON_THRESH = 10
PIX_OFF_THRESH = 10
if camera.isOpened():
    verdict, frame1 = camera.read()
    cv2.namedWindow('SpacialImage')
    if verdict:
        while (True):
            _, frame2 = camera.read()
            #determine if this is spacial or temporal
            diffFrame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY).astype('int') - cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY).astype('int')
            # do the thresholding
            total = np.sum(diffFrame < PIX_OFF_THRESH) + np.sum(diffFrame > PIX_ON_THRESH)
            diffFrame[np.where(diffFrame < (PIX_OFF_THRESH))] = -127
            diffFrame[np.where(diffFrame > (PIX_ON_THRESH))] = 128
            diffFrame += 127
            cv2.imshow('SpacialImage', diffFrame.astype('uint8'))
            # get new frame1
            frame1 = frame2
            if total > 100:
                PIX_ON_THRESH = min(50,PIX_ON_THRESH+1)
                PIX_OFF_THRESH = max(-50, PIX_OFF_THRESH-1)
            else:
                PIX_ON_THRESH = max(1,PIX_ON_THRESH-1)
                PIX_OFF_THRESH = min(-1, PIX_OFF_THRESH+1)

            print(PIX_ON_THRESH, PIX_OFF_THRESH, total)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
#make the dynamic ranges change with the number of events coming in