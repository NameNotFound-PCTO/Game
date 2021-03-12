import cv2                                                  #Library used for webcam capture
import pygame                                               #Set of Python modules designed for writing video games
import sys                                                
import random                                               #Library used to generate random numbers
import time                                                 #This module provides various time-related functions.
import numpy as np                                          #Array menagment 
import config

kernel = np.ones((8 ,8), np.uint8)                          #Matrix 8x8 for the delete the color detection imperfections

def nothing(x):                                             
    pass

cap = cv2.VideoCapture(0)                                   #Set default cam 
cv2.namedWindow("Trackbars")                                #Create and set the window's name
cap.set(10, 100)                                            #Cam's brightness

cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)   #Create a trackbar 
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)


#Load images
PLAY_BTN = pygame.image.load('images/play.png')
EASY_BTN = pygame.image.load('images/easy.png')
MEDIUM_BTN = pygame.image.load('images/medium.png')
HARD_BTN = pygame.image.load('images/hard.png')
RESTART_BTN = pygame.image.load('images/restart.png')
QUIT_BTN = pygame.image.load('images/quit.png')
MUTE_BTN = pygame.image.load('images/mute.png')
UNMUTE_BTN = pygame.image.load('images/unMute.png')

SFONDO_MENU = pygame.image.load('images/sfondoMenu.png')
SFONDO_MENU = pygame.transform.scale(SFONDO_MENU, config.DIMENSIONI)
SFONDO_GAME = pygame.image.load('images/sfondoGame.png')
SFONDO_GAME = pygame.transform.scale(SFONDO_GAME, config.DIMENSIONI)
CART_RIGHT = pygame.image.load('images/carrelloRight.png')
CART_RIGHT = pygame.transform.scale(CART_RIGHT, (config.DIM_X_CART,116))
LEGENDA_IMG = pygame.image.load('images/legenda.png')
LEGENDA_IMG = pygame.transform.scale(LEGENDA_IMG,(400, 208))
SCORE = pygame.image.load('images/score.png')

GAME_OVER = pygame.image.load('images/gameOver.png')
GAME_OVER = pygame.transform.scale(GAME_OVER,(350, 350))
POINTS_FINAL = pygame.image.load('images/pointsFinal.png')
POINTS_FINAL = pygame.transform.scale(POINTS_FINAL,(310, 75))
WIN = pygame.image.load('images/vittoria.png')


clock = pygame.time.Clock()                                 #Create an object to help track time     
                                                            
lista_img_object = ['images/ananas.png', 'images/anguria.png',            #List of fruit and obstacle images
'images/arancia.png', 'images/avocado.png', 'images/banana.png', 'images/ciliegia.png', 
'images/fragola.png', 'images/limone.png', 'images/mela.png', 'images/pera.png', 'images/bomba.png',
 'images/coltello.png', 'images/fungo.png', 'images/fungo1Up.png', 'images/meteora.png', 'images/stella.png']

lista_cuori = ['images/cuore1.png', 'images/cuore2.png', 'images/cuore3.png']    #List of life-points images

def colorDetection(oldX):                                   #Function for detect the colour 
    _, frame = cap.read()                                   #_ (bool) to control if the webcam capture of the frame is successful, frame contains the img took from the webcam
    frameFlip = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frameFlip, cv2.COLOR_BGR2HSV)        #convert the frame from BGR to HSV (H colour, S colour's saturation, V colour's brightness)

    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
    lower_blue = np.array([l_h, l_s, l_v])                  #array that contains the value of the darker blue
    upper_blue = np.array([u_h, u_s, u_v])                  #array that contains the value of the clearer blue
    mask = cv2.inRange(hsv, lower_blue, upper_blue)         #detect the colour from the HSV by the lower and the upper blue

    mask = cv2.erode(mask, kernel, iterations=5)            #delete the imperfection from the background 
    mask = cv2.dilate(mask, kernel, iterations=5)           #delete the imperfection in the colour detected 
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)#morphological trasformation of the webcam frame 


    x, y, w, h = cv2.boundingRect(opening)                  #Draw an rectangle all over the colour detected and return the position (x,y) 
                                                            #of the top left angle, width and height 

    if x == 0:                                              #If the colour isn't detected, set the x equals to the previous x position
        x = oldX
    
    result = cv2.bitwise_and(frameFlip, frameFlip, mask=mask)#Joins the mask to the frame
    
    cv2.imshow("result", result)       
    
    return x



def clear_menu(audio):                                      #re-draws the game menù 
    screen.blit(SFONDO_MENU, (0,0))
    screen.blit(LEGENDA_IMG, (0,0))
    screen.blit(PLAY_BTN, config.BTN_PLAY_POS)
    screen.blit(EASY_BTN, config.BTN_EASY_POS)
    screen.blit(MEDIUM_BTN, config.BTN_MEDIUM_POS)
    screen.blit(HARD_BTN, config.BTN_HARD_POS)
    if audio == 0:
        screen.blit(UNMUTE_BTN, config.BTN_AUDIO_POS)
    else:
        screen.blit(MUTE_BTN, config.BTN_AUDIO_POS)


def menu():                                                 #menù of the game 
    audio = 0
    clear_menu(audio)
    
    pygame.mixer.Sound.set_volume(backgroundTrack, 0.02)    #set the volume of the background track
    pygame.mixer.Sound.play(backgroundTrack, -1)            #Unlimited play of the background sound
    velocita = 0


    while True:
        _ = colorDetection(1)                               #start the webcam 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                   
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:        #control if the left mouse button is pressed 
                p_x = event.pos[0]                          #position of the mouse pointer 
                p_y = event.pos[1]
                if p_x < config.BTN_AUDIO_POS[0] + config.BTN_AUDIO_DIM[0] and p_x > config.BTN_AUDIO_POS[0] and p_y < config.BTN_AUDIO_POS[1] + config.BTN_AUDIO_DIM[1] and p_y > config.BTN_AUDIO_POS[1]:
                                                            # control if the mouse click collide with the position of the audio button,for mute or unmute the background track
                    if audio == 1:                          #unmute
                        audio = 0
                        clear_menu(audio)
                        pygame.mixer.Sound.set_volume(backgroundTrack, 0.02)
                        pygame.mixer.Sound.set_volume(unMuteTrack, 0.1)
                        pygame.mixer.Sound.play(unMuteTrack)
                    elif audio == 0:                        #mute
                        audio = 1
                        clear_menu(audio)
                        pygame.mixer.Sound.set_volume(backgroundTrack, 0)
                        pygame.mixer.Sound.set_volume(muteTrack, 0.1)
                        pygame.mixer.Sound.play(muteTrack)

                if p_x < config.BTN_PLAY_POS[0] + config.BTN_PLAY_DIM[0] and p_x > config.BTN_PLAY_POS[0] and p_y < config.BTN_PLAY_POS[1] + config.BTN_PLAY_DIM[1] and p_y > config.BTN_PLAY_POS[1]:
                                                            #control if the mouse click collide with the position of the play button
                    pygame.mixer.Sound.set_volume(clickTrack, 0.1)
                    pygame.mixer.Sound.play(clickTrack)
                    if velocita == 0:                       #if the difficulty isn't setted, the game doesn't start
                        fnt = pygame.font.SysFont("Bauhaus 93", 35)
                        surf_txt = fnt.render("Scegliere una difficolta' e poi cliccare PLAY", True, config.NERO)
                        screen.blit(surf_txt, (430, 560))
                    else:
                        return velocita                     #set the difficulty
                if p_x < config.BTN_EASY_POS[0] + config.BTN_EASY_DIM[0] and p_x > config.BTN_EASY_POS[0] and p_y < config.BTN_EASY_POS[1] + config.BTN_EASY_DIM[1] and p_y > config.BTN_EASY_POS[1]:
                                                            #control if the mouse click collide with the position of the easy button 
                    pygame.mixer.Sound.set_volume(clickTrack, 0.1)
                    pygame.mixer.Sound.play(clickTrack)
                    velocita = 3
                    clear_menu(audio)
                    fnt = pygame.font.SysFont("Bauhaus 93", 35)
                    surf_txt = fnt.render("Difficolta' selezionata: EASY", True, config.NERO)
                    screen.blit(surf_txt, (480, 560))

                if p_x < config.BTN_MEDIUM_POS[0] + config.BTN_MEDIUM_DIM[0] and p_x > config.BTN_MEDIUM_POS[0] and p_y < config.BTN_MEDIUM_POS[1] + config.BTN_MEDIUM_DIM[1] and p_y > config.BTN_MEDIUM_POS[1]:
                                                        #control if the mouse click collide with the position of the medium button
                    pygame.mixer.Sound.set_volume(clickTrack, 0.1)
                    pygame.mixer.Sound.play(clickTrack)
                    velocita = 5
                    clear_menu(audio)
                    fnt = pygame.font.SysFont("Bauhaus 93", 35)
                    surf_txt = fnt.render("Difficolta' selezionata: MEDIUM", True, config.NERO)
                    screen.blit(surf_txt, (480, 560))

                if p_x < config.BTN_HARD_POS[0] + config.BTN_HARD_DIM[0] and p_x > config.BTN_HARD_POS[0] and p_y < config.BTN_HARD_POS[1] + config.BTN_HARD_DIM[1] and p_y > config.BTN_HARD_POS[1]:
                                                        #control if the mouse click collide with the position of the hard button
                    pygame.mixer.Sound.set_volume(clickTrack, 0.1)
                    pygame.mixer.Sound.play(clickTrack)
                    velocita = 7
                    clear_menu(audio)
                    fnt = pygame.font.SysFont("Bauhaus 93", 35)
                    surf_txt = fnt.render("Difficolta' selezionata: HARD", True, config.NERO)
                    screen.blit(surf_txt, (480, 560))
                    
        
        pygame.display.update()


def stampaVite(vite):                                   #print the image of the life points
    imgVite = lista_cuori[vite-1]
    screen.blit(pygame.image.load(imgVite), (config.COORD_CUORI[0], config.COORD_CUORI[1]))



def stampaFrutta(xFrutta,yFrutta,frutta,velocita,xCart, yCart, dimXCart, dimXFrutta, dimYFrutta, punteggio, vite):
                                                        #manage the obstacles and fruit drop
    screen.blit(SFONDO_GAME,(0,0))
    screen.blit(LEGENDA_IMG, (0,0))
    screen.blit(SCORE, (1200, 90))
    screen.blit(pygame.image.load(frutta),(xFrutta,yFrutta))
    stampaVite(vite)
    fnt = pygame.font.SysFont("Bauhaus 93", 85)
    surf_txt = fnt.render(str(punteggio), True, config.NERO)
    if punteggio >= 10:
        screen.blit(surf_txt, (1290, 190))
    else:
        screen.blit(surf_txt, (1320, 190))

    

    if yFrutta <= (config.DIMENSIONI[1] - 160) and raccolto(xCart, yCart, dimXCart, xFrutta, yFrutta, dimXFrutta, dimYFrutta) == False:
                                                    #if the y position of the object doesn't collide with the cart or the floor, the y position is updated 
        yFrutta += velocita
    else:                                           #if the object is in the cart or on the floor, we generate a new object to drop                                          
        if raccolto(xCart, yCart, dimXCart, xFrutta, yFrutta, dimXFrutta, dimYFrutta):
                                                    #object is in the cart
            if str(frutta) == 'images/meteora.png' or str(frutta) == 'images/coltello.png' or str(frutta) == 'images/fungo.png':
                                                    #if the object is an obstacles, the life points is decreased
                pygame.mixer.Sound.set_volume(missTrack, 0.1)
                pygame.mixer.Sound.play(missTrack)
                vite -= 1
            elif str(frutta) == 'images/bomba.png':
                pygame.mixer.Sound.set_volume(bombTrack, 0.1)
                pygame.mixer.Sound.play(bombTrack)
                vite -= 1
            elif str(frutta) == 'images/fungo1Up.png' and vite != 3:
                                                    #if the object is the good mushroom, the life point is increased (life max=3)
                vite += 1
                pygame.mixer.Sound.set_volume(fungoTrack, 0.1)
                pygame.mixer.Sound.play(fungoTrack)
                
            elif str(frutta) == 'images/stella.png':
                                                    #if the object is the star, the score is increased by 3
                pygame.mixer.Sound.set_volume(starTrack, 0.1)
                pygame.mixer.Sound.play(starTrack)
                punteggio += 3      
            else:                           
                                                    #if the object is a normal fruit, the score is increased by 1
                pygame.mixer.Sound.set_volume(raccoltoTrack, 0.1)
                pygame.mixer.Sound.play(raccoltoTrack)
                punteggio += 1
        elif str(frutta) != 'images/bomba.png' and str(frutta) != 'images/meteora.png' and str(frutta) != 'images/coltello.png' and str(frutta) != 'images/fungo.png' and str(frutta) != 'images/stella.png' and str(frutta) != 'images/fungo1Up.png':
                                                    #if an fruit drop on the flor, the life point is decreased
            pygame.mixer.Sound.set_volume(missTrack, 0.1)
            pygame.mixer.Sound.play(missTrack)
            vite -= 1
        if vite == 0:                               #if the life point are 0, the game is over
            gameOver(punteggio)
        if punteggio >= 30:                         #if the score is more or equals than 30, the player win 
            vittoria(punteggio)

        fruttaScelta=random.randint(0,15)           
        frutta=lista_img_object[fruttaScelta]
        yFrutta=0
        xFrutta=random.randint(config.COORD_X_FRUTTA[0], config.COORD_X_FRUTTA[1])
    

    return xFrutta,yFrutta,frutta,punteggio,vite


def raccolto(xCart, yCart, dimXCart, xFrutta, yFrutta, dimXFrutta, dimYFrutta):
                                                    #if the position of the obstacles collide with the cart, return true
    if (xFrutta + (dimXFrutta/2) > xCart and xFrutta+(dimXFrutta/2) < xCart + dimXCart) and (yFrutta + dimYFrutta-40 < yCart + 8 and yFrutta + dimYFrutta - 40 > yCart):                  #coordinate impatto frutta con il carrello
        return True
    else:
        return False



def gioco(punteggio, vite, velocita):               #game 
    screen.blit(SFONDO_GAME, (0,0))                 #print the game's background 
    screen.blit(LEGENDA_IMG, (0,0))
                                                    #fist random object to drop of the game 
    xFrutta = random.randint(config.COORD_X_FRUTTA[0], config.COORD_X_FRUTTA[1])
    yFrutta = 0
    fruttaRand = random.randint(0, 15)
    img = lista_img_object[fruttaRand]
    xCam = 200

    
    while True :
        xCam = colorDetection(xCam)                 #position detected
        xFrutta, yFrutta, img, punteggio, vite = stampaFrutta(xFrutta, yFrutta, img, velocita,xCam + config.COORD_X_FRUTTA[0]-30, 640, config.DIM_X_CART, config.DIM_FRUTTA[0], config.DIM_FRUTTA[1], punteggio, vite)
        screen.blit(CART_RIGHT, (xCam + config.COORD_X_FRUTTA[0]-30, 650))
                                                    #print the cart
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
            
        clock.tick(60)
        
        pygame.display.update()



def gameOver(punteggio):                            #when the player lose
    pygame.mixer.Sound.set_volume(gameOverTrack, 0.1)
    pygame.mixer.Sound.play(gameOverTrack)
    screen.blit(SFONDO_GAME, (0,0))
    screen.blit(GAME_OVER, (config.COORD_GAMEOVER[0], config.COORD_GAMEOVER[1]))
    screen.blit(POINTS_FINAL, (config.COORD_POINTS_FINAL[0], config.COORD_POINTS_FINAL[1]))
    fnt = pygame.font.SysFont("Bauhaus 93", 85)
    surf_txt = fnt.render(str(punteggio), True, config.NERO)
    screen.blit(surf_txt, (config.COORD_POINTS_FINAL[0] + 340, config.COORD_POINTS_FINAL[1]-5))
    screen.blit(config.RESTART_BTN, config.BTN_RESTART_POS)
    screen.blit(QUIT_BTN, config.BTN_QUIT_POS)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:#control if the player want restart a game or quit   
                p_x = event.pos[0]
                p_y = event.pos[1]
                if p_x < config.BTN_RESTART_POS[0] + config.BTN_RESTART_DIM[0] and p_x > config.BTN_RESTART_POS[0] and p_y < config.BTN_RESTART_POS[1] + config.BTN_RESTART_DIM[1] and p_y > config.BTN_RESTART_POS[1]:
                    pygame.mixer.Sound.set_volume(clickTrack, 0.1)
                    pygame.mixer.Sound.play(clickTrack)
                    pygame.mixer.stop()
                    main()
                elif p_x < config.BTN_QUIT_POS[0] + config.BTN_QUIT_DIM[0] and p_x > config.BTN_QUIT_POS[0] and p_y < config.BTN_QUIT_POS[1] + config.BTN_QUIT_DIM[1] and p_y > config.BTN_QUIT_POS[1]:
                    pygame.mixer.Sound.set_volume(clickTrack, 0.1)
                    pygame.mixer.Sound.play(clickTrack)
                    pygame.quit()
                    sys.exit()
                    cap.release()
                    cv2.destroyAllWindows()
        pygame.display.update()



def vittoria(punteggio):                            #when the player win
    pygame.mixer.Sound.set_volume(winTrack, 0.1)
    pygame.mixer.Sound.play(winTrack)
    screen.blit(SFONDO_GAME, (0,0))
    screen.blit(WIN, (config.COORD_WIN[0], config.COORD_WIN[1]))
    screen.blit(POINTS_FINAL, (config.COORD_POINTS_FINAL[0], config.COORD_POINTS_FINAL[1]))
    fnt = pygame.font.SysFont("Bauhaus 93", 85)
    surf_txt = fnt.render(str(punteggio), True, config.NERO)
    screen.blit(surf_txt, (config.COORD_POINTS_FINAL[0] + 340, config.COORD_POINTS_FINAL[1]-5))
    screen.blit(RESTART_BTN, config.BTN_RESTART_POS)
    screen.blit(QUIT_BTN, config.BTN_QUIT_POS)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:#control if the player want restart a game or quit 
                p_x = event.pos[0]
                p_y = event.pos[1]
                if p_x < config.BTN_RESTART_POS[0] + config.BTN_RESTART_DIM[0] and p_x > config.BTN_RESTART_POS[0] and p_y < config.BTN_RESTART_POS[1] + config.BTN_RESTART_DIM[1] and p_y > config.BTN_RESTART_POS[1]:
                    pygame.mixer.Sound.set_volume(clickTrack, 0.1)
                    pygame.mixer.Sound.play(clickTrack)
                    main()
                elif p_x < config.BTN_QUIT_POS[0] + config.BTN_QUIT_DIM[0] and p_x > config.BTN_QUIT_POS[0] and p_y < config.BTN_QUIT_POS[1] + config.BTN_QUIT_DIM[1] and p_y > config.BTN_QUIT_POS[1]:
                    cap.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

                    

def main():
    global screen
    pygame.init()
    
    #initialate the music and the sound effect
    global backgroundTrack
    backgroundTrack = pygame.mixer.Sound("sounds/background_game.mp3")
    global clickTrack
    clickTrack = pygame.mixer.Sound("sounds/click.wav")
    global raccoltoTrack
    raccoltoTrack = pygame.mixer.Sound("sounds/raccolto.wav")
    global missTrack
    missTrack = pygame.mixer.Sound("sounds/miss.wav")
    global starTrack
    starTrack = pygame.mixer.Sound("sounds/star.wav")
    global bombTrack
    bombTrack = pygame.mixer.Sound("sounds/bomb.wav")
    global fungoTrack
    fungoTrack = pygame.mixer.Sound("sounds/fungo.wav")
    global unMuteTrack
    unMuteTrack = pygame.mixer.Sound("sounds/unMute.wav")
    global muteTrack
    muteTrack = pygame.mixer.Sound("sounds/mute.wav")
    global gameOverTrack
    gameOverTrack = pygame.mixer.Sound("sounds/gameOver.wav")
    global winTrack
    winTrack = pygame.mixer.Sound("sounds/win.wav")

    screen = pygame.display.set_mode(config.DIMENSIONI)
    screen.fill(config.NERO)
    punteggio = 0
    global vite
    vite = 3

    while True:
        velocita = menu()
        gioco(punteggio, vite, velocita)
        pygame.display.update()

if __name__ == "__main__":
    main()               