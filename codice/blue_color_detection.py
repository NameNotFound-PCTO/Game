import cv2
import numpy as np

kernel = np.ones((8 ,8), np.uint8)

def nothing(x):
    pass

cap = cv2.VideoCapture(0)       #utilizza cam di default (0)
cv2.namedWindow("Trackbars")
'''cap.set(3, 640)
cap.set(4, 480)'''
cap.set(10, 100)        #lucentezza della cam

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

     

'''    #min = [0, 0, 0]         max e min scala colori openCV
    #max = [180, 255, 255]
'''
    
while True:
    _, frame = cap.read()       # _ bool per vedere se la cattura dal frame dalla cam ha avuto successo o meno, img frame della cam
    frameFlip = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frameFlip, cv2.COLOR_BGR2HSV)       #converto il frame da BGR in HSV    (H colore, S concentrazione colore, V lucentezza colore)

    
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    mask = cv2.erode(mask, kernel, iterations=5)
    mask = cv2.dilate(mask, kernel, iterations=5)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    x, y, w, h = cv2.boundingRect(opening)

    print(x,"1")
    
    result = cv2.bitwise_and(frameFlip, frameFlip, mask=mask)
    
    cv2.imshow("frame", frameFlip)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)       

    if cv2.waitKey(1) == 27:        #controllo se nel millisecondo è stato schiacciato esc (27) esce dal loop e chiude tutte le finestre
        break

cap.release()
cv2.destroyAllWindows()
