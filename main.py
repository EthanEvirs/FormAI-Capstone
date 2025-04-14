import pygame
import math
import button
from button import Button
import os
import cv2
import mediapipe as mp
import numpy as np
from camera import Camera


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
TEXT = pygame.mixer.Sound("text.wav")
# VICTORY = pygame.mixer.Sound("WIN.mp3")
# VICTORY2 = pygame.mixer.Sound("WIN2.mp3")

#IMAGES
STARTLOGO = pygame.image.load("MAINLOGOUPDATE.png")
BACKGROUND = pygame.image.load("background.jpeg")
LOGO = pygame.image.load("formai.png").convert_alpha()
BUTTON1 = pygame.image.load("BicepCurl1.png").convert_alpha()
BUTTON2 = pygame.image.load("BicepCurl2.png").convert_alpha()
BUTTON3 = pygame.image.load("MilitaryPress2.png").convert_alpha()
BUTTON4 = pygame.image.load("MilitaryPress3.png").convert_alpha()
BUTTON5 = pygame.image.load("FrontRaise1.png").convert_alpha()
BUTTON6 = pygame.image.load("FrontRaise2.png").convert_alpha()

#CHARACTER
MILSTANDING1 = pygame.image.load("mil1.jpeg").convert_alpha()
MILSTANDING2 = pygame.image.load("mil2.jpeg").convert_alpha()
REDSTANDING1 = pygame.image.load("red2.jpeg").convert_alpha()
REDSTANDING2 = pygame.image.load("red2.jpeg").convert_alpha()



bicep_curls = button.Button(80, 200, BUTTON1, 0.8, hover_image=BUTTON2)
military_button = button.Button(80, 300, BUTTON3, 0.8, hover_image=BUTTON4)
front_button = button.Button(80, 100, BUTTON5, 0.8, hover_image=BUTTON6)

scroll = 0
tiles = math.ceil(width / BACKGROUND.get_width()) + 1


def show_start_menu():
    pygame.mixer.music.load("INTRO.mp3")
    pygame.mixer.music.set_volume(0.5)
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
                
def military_press_cutscene():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("Military.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    font = pygame.font.SysFont(None, 24)

    messages = [
        "YOOOO you think you got what it takes to out lift me fooo",
        "LETS SEE WHATACHA GOT",
        "I AINT sEE NO ONE LIKE YOU AROUND HERE",
        "GOODLUCKKKK"
    ]
    
    message_index = 0
    space_press_count = 0  # Count number of space presses

    # Add your animation frames here
    mil_frames = [MILSTANDING1, MILSTANDING2]  # Replace with your actual frame surfaces

    rect_x, rect_y, rect_w, rect_h = 55, 272, 300, 64

    def wrap_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        return lines

    while True:
        screen.fill((0,0,0))

        # Pick the current MIL frame based on space_press_count // 2
        current_frame_index = min(space_press_count // 2, len(mil_frames) - 1)
        screen.blit(mil_frames[current_frame_index], (0, 0))

        pygame.draw.rect(screen, (95,205,228), (rect_x, rect_y, rect_w, rect_h))

        if message_index < len(messages):
            wrapped_lines = wrap_text(messages[message_index], font, rect_w - 10)
            for i, line in enumerate(wrapped_lines):
                line_surface = font.render(line, True, (0, 0, 0))
                screen.blit(line_surface, (rect_x + 5, rect_y + 5 + i * font.get_height()))
        else:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("MENU.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            # pygame.mixer.Sound.set_volume(VICTORY, 0.5)
            # pygame.mixer.Sound.play(VICTORY)
            return

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    message_index += 1
                    space_press_count += 1  # Only increment by 1
                    pygame.mixer.Sound.set_volume(TEXT, 0.8)
                    pygame.mixer.Sound.play(TEXT)


def bicep_curl_cutscene():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("red.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    font = pygame.font.SysFont(None, 24)
    
    messages = [
        "You must be the new guy, I've been hearing about!?",
        "Say new guy you think you have what it takes to hit 8 perfect reps",
        "Most fresh meat cant get past 2 hahahah.",
        "I'd like to see you try!"
    ]
    
    message_index = 0
    space_press_count = 0  # Count number of space presses
    
    # Add your animation frames here
    red_frames = [REDSTANDING1, REDSTANDING2]
    rect_x, rect_y, rect_w, rect_h = 55, 272, 300, 64
    
    def wrap_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
    
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        return lines
    
    while True:
        screen.fill((0,0,0))
    
        # Pick the current MIL frame based on space_press_count // 2
        current_frame_index = min(space_press_count // 2, len(red_frames) - 1)
        screen.blit(red_frames[current_frame_index], (0, 0))
    
        pygame.draw.rect(screen, (172,50,50), (rect_x, rect_y, rect_w, rect_h))
    
        if message_index < len(messages):
            wrapped_lines = wrap_text(messages[message_index], font, rect_w - 10)
            for i, line in enumerate(wrapped_lines):
                line_surface = font.render(line, True, (0, 0, 0))
                screen.blit(line_surface, (rect_x + 5, rect_y + 5 + i * font.get_height()))
        else:
            
            pygame.mixer.music.stop()
            start_bicep_curl_pose()
            pygame.mixer.music.load("MENU.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            # pygame.mixer.Sound.set_volume(VICTORY2, 0.5)
            # pygame.mixer.Sound.play(VICTORY2)
            
            return
    
        pygame.display.flip()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    message_index += 1
                    space_press_count += 1  # Only increment by 1
                    pygame.mixer.Sound.set_volume(TEXT, 0.8)
                    pygame.mixer.Sound.play(TEXT)
                    
def start_bicep_curl_pose():
    pygame.mixer.music.load("CAMERA.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    camera = Camera()
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    screen = pygame.display.set_mode((800, 600))  # Resize to fit both preview + camera
    pygame.display.set_caption("Bicep Curl Tracker")

    font = pygame.font.SysFont(None, 36)

    def draw_text(surface, text, pos, color=(255, 255, 255)):
        img = font.render(text, True, color)
        surface.blit(img, pos)

    running = True
    while running:
        ret, frame = camera.cam.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Blank preview image
        pose_preview = np.zeros((480, 480, 3), dtype=np.uint8)

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            mp.solutions.drawing_utils.draw_landmarks(pose_preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = np.rot90(frame_rgb)
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        frame_surface = pygame.transform.scale(frame_surface, (400, 400))

        preview_rgb = cv2.cvtColor(pose_preview, cv2.COLOR_BGR2RGB)
        preview_rgb = np.rot90(preview_rgb)
        preview_surface = pygame.surfarray.make_surface(preview_rgb)
        preview_surface = pygame.transform.scale(preview_surface, (200, 200))

        screen.fill((128, 0, 128))  # Purple background
        screen.blit(preview_surface, (25, 50))
        screen.blit(frame_surface, (250, 50))
        draw_text(screen, "ESC to exit", (50, 470))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return

    camera.release()
    pygame.display.set_mode((400, 400))  # Reset window size when done


show_start_menu()
pygame.mixer.music.load("MENU.mp3")
pygame.mixer.music.set_volume(0.5)
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
        bicep_curl_cutscene()

    if military_button.draw(screen):
        print("Military Press")
        pygame.mixer.Sound.play(OPENSOUND)
        military_press_cutscene()

    if front_button.draw(screen):
        print("FrontRaise")
        pygame.mixer.Sound.play(OPENSOUND)
    

    # flip() the display to put your work on screen
    screen.blit(LOGO, (70,0))
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()