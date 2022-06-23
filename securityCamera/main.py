import cv2
import pygame
import beepy



def initAlert():
    pygame.init()
    pygame.mixer.init()
    global sounda
    sounda = pygame.mixer.Sound("caution.wav")
    sounda.stop()

def playAlert():
    sounda.play()


def videoCapture():
    cam = cv2.VideoCapture(0)
    initAlert()
    while cam.isOpened():
        ret, frame1 = cam.read()
        ret, frame2 = cam.read()
        diff = cv2.absdiff(frame1, frame2)
        grayDiff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blurGray = cv2.GaussianBlur(grayDiff, (5,5), 0)
        _, thresh = cv2.threshold(blurGray, 20, 255, cv2.THRESH_BINARY) #removes noise, take values from 20 to 255
        dialated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dialated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
       # cv2.drawContours(frame1, contours, -1, (255,0,0), 2)

        for c in contours:
            if cv2.contourArea(c) < 10000: #small object movements ignored
                continue
            x,y, height, width = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x,y), (x+height,y+width), (255,0,0), 2)
            playAlert()

        if cv2.waitKey(5) == ord('x'):
            break
        cv2.imshow('Security Camera', frame1)





videoCapture()