import pygame
import math
import button
from button import Button
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'


# pygame setup
pygame.init()
info = pygame.display.Info()
width = 400
height = 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("FORM-AI")
pygame.mixer.init()
#SOUNDS
OPENSOUND = pygame.mixer.Sound("open.wav")
PICK= pygame.mixer.Sound("Pick.mp3")
START = pygame.mixer.Sound("START.mp3")

#IMAGES
STARTLOGO = pygame.image.load("MAINLOGO.jpeg")
BACKGROUND = pygame.image.load("background.jpeg")
LOGO = pygame.image.load("formai.png").convert_alpha()
BUTTON1 = pygame.image.load("BicepCurl1.png").convert_alpha()
BUTTON2 = pygame.image.load("BicepCurl2.png").convert_alpha()
BUTTON3 = pygame.image.load("MilitaryPress2.png").convert_alpha()
BUTTON4 = pygame.image.load("MilitaryPress3.png").convert_alpha()
BUTTON5 = pygame.image.load("FrontRaise1.png").convert_alpha()
BUTTON6 = pygame.image.load("FrontRaise2.png").convert_alpha()

bicep_curls = button.Button(80, 200, BUTTON1, 0.8, hover_image=BUTTON2)
military_button = button.Button(80, 300, BUTTON3, 0.8, hover_image=BUTTON4)
front_button = button.Button(80, 100, BUTTON5, 0.8, hover_image=BUTTON6)

scroll = 0
tiles = math.ceil(width / BACKGROUND.get_width()) + 1


def show_start_menu():
    pygame.mixer.music.load("INTRO.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    while True:
        screen.blit(STARTLOGO, (0,0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.Sound.set_volume(START, 0.3)
                    pygame.Sound.play(START)
                    pygame.mixer.music.stop()
                    pygame.time.delay(2000)
                    return 

show_start_menu()
pygame.mixer.music.load("MENU.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)
pygame.mixer.Sound.set_volume(PICK, 0.3)
pygame.mixer.Sound.play(PICK)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    i = 0
    while (i < tiles):
        screen.blit(BACKGROUND, (BACKGROUND.get_width() * i + scroll, 0))
        i += 1
    
    scroll -= 6

    if abs(scroll) >  BACKGROUND.get_width():
        scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame

    # RENDER YOUR GAME HERE
    if bicep_curls.draw(screen):
        print("Bicep_Curls")
        pygame.mixer.Sound.play(OPENSOUND)

    if military_button.draw(screen):
        print("Military Press")
        pygame.mixer.Sound.play(OPENSOUND)

    if front_button.draw(screen):
        print("FrontRaise")
        pygame.mixer.Sound.play(OPENSOUND)
    

    # flip() the display to put your work on screen
    screen.blit(LOGO, (70,0))
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()