from doctest import master
from shutil import move
from tkinter import W
from cvzone.HandTrackingModule import HandDetector
import HandTrackingModule as htm
import math
import cv2
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from datetime import datetime
import time
import numpy as np
#import autopy
import pynput
import imutils
#import wx


from collections import deque
import cvzone

from pynput.mouse import Button, Controller

## SETTINGS
wScr, hScr = 1920, 1080
smoothening = 7
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = HandDetector(detectionCon=0.8, maxHands=2)
pTime = 0
 
frameR = 150 # Frame Reduction
plocX, plocY = 0, 0
clocX, clocY = 0, 0

mouse = Controller()



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0


index = [0,1,0,0,0]
middle = [0,0,1,0,0]
closed = [0,0,0,0,0]
custom1 = [1,1,1,0,0]
custom2 = [1,1,1,1,1]
custom3 = [0,1,1,0,0]

activate_volume_on = False


def open_spotify(fingers1):

    start_now = datetime.now()

    global activate_spotify_on
    activate_spotify_on  = False 
    

    # if  handType1 == "Right" :
    #     if (fingers1 == custom2)  and (((datetime.now - start_now) > 1) and ((datetime.now - start_now) <5) ) : 
    #         if fingers1 == closed and (((datetime.now - start_now) > 5) and ((datetime.now - start_now) <10) ) :
    #             print(start_now)





def activate_volume_controls(start_now,fingers1):

    global activate_volume_on
    activate_volume_on = False 

    start_time_seconds =  int(start_now.strftime("%S"))
    #print(start_time_seconds)

    if  (fingers1 == closed) and handType1 == "Right":
        now = datetime.now()
        current_time = datetime.now()
        current_time_seconds = int(now.strftime("%S"))
        #print(current_time_seconds)
        #print("RECORDING")
        
        if activate_volume_on == True :
            activate_volume_on = False
            #print("NOT RECORDING")

        activate_volume_on = True
        
        #cv2.putText(img, f'RECORDING RIGHT HAND', (40,70), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
    
def activate_cursor_controls(start_now,fingers1):

    global activate_cursor_on
    activate_cursor_on = False 

    start_time_seconds =  int(start_now.strftime("%S"))
    #print(start_time_seconds)

    if  (fingers1 == [0,1,1,0,0]) and handType1 == "Right":
        now = datetime.now()
        current_time = datetime.now()
        current_time_seconds = int(now.strftime("%S"))
        #print(current_time_seconds)
        #print("CURSOR_ACTIVATED")
        
        if activate_cursor_on == True :
            activate_cursor_on = False
            #print("CURSOR ACTIVATED")

        activate_cursor_on = True
        
        #cv2.putText(img, f'RECORDING RIGHT HAND', (40,70), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
      
def cursor_click(click_length):
    global cursor_cl
    cursor_cl = False

    if click_length > 40 :

    

        
       
        mouse.press(Button.left)
        mouse.release(Button.left)

        


while True:
    

    #LmList = detector.findPosition(img, draw=False)

    # Get image frame
    success, img = cap.read()
    #print(img)
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    
    # 2. Get the tip of the index and middle fingers
    
    
    # hands = detector.findHands(img, draw=False)  # without draw
    
    # x1, y1 = LmList[4] [1] , LmList[4][2]
    # x2, y2 = lmList[8][1], LmList[8][2]
    # cv2.circle(img, (x1, y1) , 15, (255, 0 , 255) , cv2.FILLED)
    # cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

    if hands:

        

        #hands, bbox = detector.findPosition(img, draw=False)

        #print(bbox)
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        fingers1 = detector.fingersUp(hand1)
        #face = detector.findDistance

        #print(lmList1[4],lmList1[8])
        

        

        if len(hands) == 2 :

            lmList2, bbox = detector.findPosition(img)
            
            
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmark points
            bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"
            fingers2 = detector.fingersUp(hand2)

            #area = (bbox1[2] - bbox1[0]) * (bbox2[3] - bbox2[1]) # 100


            ## SORT HANDS
            

            if handType1 == "Right" :
                ## RIGHT HAND IS ALWAYS 0 LEFT IS 1
                ## MAKE HAND TYPE1 ALWAYS RIGHT

                hand1 = hands[0]
                lmList1 = hand1["lmList"]  # List of 21 Landmark points
                bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
                centerPoint1 = hand1['center']  # center of the hand cx,cy
                handType1 = hand1["type"]  # Handtype Left or Right
                fingers1 = detector.fingersUp(hand1)

                hand2 = hands[1]
                lmList2 = hand2["lmList"]  # List of 21 Landmark points
                bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
                centerPoint2 = hand2['center']  # center of the hand cx,cy
                handType2 = hand2["type"]  # Hand Type "Left" or "Right"
                fingers2 = detector.fingersUp(hand2)

                
            if handType1 == "Left" :

                hand1 = hands[1]
                lmList1 = hand1["lmList"]  # List of 21 Landmark points
                bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
                centerPoint1 = hand1['center']  # center of the hand cx,cy
                handType1 = hand1["type"]  # Handtype Left or Right
                fingers1 = detector.fingersUp(hand1)


                hand2 = hands[0]
                lmList2 = hand2["lmList"]  # List of 21 Landmark points
                bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
                centerPoint2 = hand2['center']  # center of the hand cx,cy
                handType2 = hand2["type"]  # Hand Type "Left" or "Right"
                fingers2 = detector.fingersUp(hand2)

            
            if (handType1 == "Right") :
                    start_now = datetime.now()
                    activate_volume_controls(start_now,fingers1)
                    

            # if len(lmList) != 0:
           
            #x2, y2 = lmList2[12][1:] #middle 
            # print(x1, y1, x2, y2 )

            ## IF CONTROLS ARE TRUE

            # print(bbox1[2])
            # print(bbox1[3])

            area = bbox1[2] * bbox1[3]

            dist_z = (1/(area))*1000

            #print(f'{dist_z : .1g}')

            dist_z = float(str(f'{dist_z : .1g}'))

            dist_scale = 1/dist_z
            #print(f'{dist_scale : .1g}')

            

            if activate_volume_on == True :
                
               

                cv2.putText(img, f'ACTIVATED VOLUME SETTINGS', (40,70), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
                #length_pi, info, img = detector.findDistance(lmList2[8][:2], lmList2[12][:2], img)  # with draw
                #length_pi = math.hypot(lmList2[8][1]-lmList2[12][1],lmList2[8][2] - lmList2[12][2])

                if (handType2 == "Left") :

                    #Find Distance between two Landmarks. Could be same hand or different hands
                    length, info, img = detector.findDistance(lmList2[4][:2], lmList2[8][:2], img)  # with draw
                    length = math.hypot(lmList2[8][1]-lmList2[4][1],lmList2[8][2] - lmList2[4][2])
                    # length, info = detector.findDistance(lmList2[8], lmList2[8])  # with draw

                    
                    
                    
                     # np.interp(length, [50, 200], [minVol, maxVol])
                    volBar = np.interp(length, [0, 100], [400, 150])
                    volPer = np.interp(length, [0, 100], [0, 100])
                    smoothness = 10 

                        
                    
                    
                    # smoothness = 100 * (dist_z)
                    volPer = smoothness * round(volPer / smoothness) 

                    vol_final = float(volPer/100)
                    updated_volume = min(1.0, max(0.0, volPer))
                    

                    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
                    cv2.putText(img, f'{(vol_final)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)
                    
                    #volume.SetMasterVolumeLevel(vol, None)
                    
                    volume.SetMasterVolumeLevelScalar(volPer/100, None)

            # if activate_cursor_on == True :

            #         x1 = lmList2[8][0]
            #         y1 = lmList2[8][1] 

            #         # x3 = np.interp(x1, (0,wCam), (0, wScr))
            #         # y3 = np.interp(y1, (0,wCam), (0, hScr))
            #         x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            #         y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            #         clocX = plocX + (x3 - plocX) / smoothening
            #         clocY = plocY + (y3 - plocY) / smoothening
            #         cv2.putText(img, f'ACTIVATED CURSOR SETTINGS : {x1} , {y1}', (40,70), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
            #         cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
            #         cv2.circle(img, (x1, y1) , 15, (255, 0 , 255) , cv2.FILLED)
                   

            #         mouse.position = (wScr-clocX,clocY)
            #         plocX, plocY = clocX, clocY
            #         print(x3,y3)
            

            



                

            
        if len(hands) == 1 :


            if (handType1 == "Right") :
                start_now = datetime.now() 
                activate_volume_controls(start_now,fingers1)
                activate_cursor_controls(start_now,fingers1)
                
                open_spotify(fingers1)

                if activate_volume_on == True :
                    cv2.putText(img, f'ACTIVATED SETTINGS', (40,70), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
        
                # if  fingers1 == [1,0,0,0,1] :
                #     cv2.destroyAllWindows()
                #     break
            
                if activate_cursor_on == True :
                    x1 = lmList1[8][0]
                    y1 = lmList1[8][1] 

                    x2 = lmList1[12][0]
                    y2 = lmList1[12][1]

                    # x3 = np.interp(x1, (0,wCam), (0, wScr))
                    # y3 = np.interp(y1, (0,wCam), (0, hScr))
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening

                    cx ,cy = int(centerPoint1[0]), int(centerPoint1[1])

                    cv2.putText(img, f'ACTIVATED CURSOR SETTINGS : {x1} , {y1}', (40,70), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
                    #cv2.rectangle(img,((cx),(cy)),((x3,y3)),(255, 0, 255), 2)
                    cv2.circle(img, centerPoint1 , 15, (255, 0 , 255) , cv2.FILLED)
                   

                    mouse.position = (wScr-clocX,clocY)
                    plocX, plocY = clocX, clocY
                    print(centerPoint1[0])


                    length, info, img = detector.findDistance(lmList1[8][:2], lmList1[12][:2], img)
                    cursor_click(length)
                
                if activate_spotify_on == True :
                    cv2.putText(img, f'OPENING SPOTIFY', (40,70), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)

    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255,248,220), 1)           
        
            
    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    
cap.release()
cv2.destroyAllWindows()