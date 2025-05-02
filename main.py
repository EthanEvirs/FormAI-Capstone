import pygame
import math
import button
from button import Button
import os
import cv2
import mediapipe as mp
import numpy as np
import requests
import re
from camera import Camera

#supervised learning model
os.environ['SDL_VIDEO_CENTERED'] = '1'

# pygame setup
pygame.init()
info = pygame.display.Info()
width = 800
height = 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("FORM-AI")
pygame.mixer.init()
#SOUNDS
OPENSOUND = pygame.mixer.Sound("Sounds/open.wav")
PICK= pygame.mixer.Sound("Sounds/Pick.mp3")
START = pygame.mixer.Sound("Sounds/START.mp3")
TEXT = pygame.mixer.Sound("Sounds/text.wav")
# VICTORY = pygame.mixer.Sound("WIN.mp3")
# VICTORY2 = pygame.mixer.Sound("WIN2.mp3")

victorycounter = 0
goodrepright = 0
badrepright = 0
goodrepleft = 0
badrepleft = 0
username = ""

def load_and_scale(path, scale=2):
    img = pygame.image.load(path).convert_alpha()
    img_width, img_height = img.get_size()
    return pygame.transform.scale(img, (int(img_width * scale), int(img_height * scale)))

#IMAGES
INTROBACKGROUND = load_and_scale("Resource/INTROBACKGROUND.jpeg")
STARTLOGO = load_and_scale("Resource/MAINLOGOUPDATE.png")
BACKGROUND = load_and_scale("Resource/background.jpeg")
LOGO = load_and_scale("Resource/formai.png")
BUTTON1 = load_and_scale("Resource/BicepCurl1.png")
BUTTON2 = load_and_scale("Resource/BicepCurl2.png")
BUTTON3 = load_and_scale("Resource/MilitaryPress2.png")
BUTTON4 = load_and_scale("Resource/MilitaryPress3.png")
BUTTON5 = load_and_scale("Resource/FrontRaise1.png")
BUTTON6 = load_and_scale("Resource/FrontRaise2.png")

# CHARACTER
MILSTANDING1 = load_and_scale("Resource/mil1.jpeg")
MILSTANDING2 = load_and_scale("Resource/mil2.jpeg")
REDSTANDING1 = load_and_scale("Resource/redd.jpeg")
REDSTANDING2 = load_and_scale("Resource/redd.jpeg")
LUSTANDING1 = load_and_scale("Resource/raises1.jpeg")
LUSTANDING2 = load_and_scale("Resource/raises2.jpeg")


center_x = (800 - BUTTON1.get_width()) // 2

bicep_curls = button.Button(center_x, 200, BUTTON1, 0.8, hover_image=BUTTON2)
military_button = button.Button(center_x, 200 + BUTTON1.get_height() - 80, BUTTON3, 0.8, hover_image=BUTTON4)
front_button = button.Button(center_x, 200 + BUTTON1.get_height() + 80, BUTTON5, 0.8, hover_image=BUTTON6)

scroll = 0
tiles = math.ceil(width / BACKGROUND.get_width()) + 1

def sanitize_username(name):
    name = name.strip()
    name = name[:20]
    name = re.sub(r'[^a-zA-Z0-9 ]', '', name)
    return name
    

def submit_score(username, goodrepright, badrepright, goodrepleft, badrepleft):
    url = "https://ethanevirs.cikeys.com/submit_reps.php"  

    data = {
        'username': username,
        'good_reps_right': goodrepright,
        'bad_reps_right': badrepright,
        'good_reps_left': goodrepleft,
        'bad_reps_left': badrepleft
    }

    try:
        response = requests.post(url, data=data)
        print("Server response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Failed to submit score:", e)

def show_start_menu():
    pygame.mixer.music.load("Sounds/INTRO.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while True:
        screen.blit(INTROBACKGROUND, (0,0))
        screen.blit(LOGO, (120,0))
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

def front_raise_curscene():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("Sounds/girl.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    font = pygame.font.Font("Fonts/pictochat.otf", 48)
    messages = [
        "HIIIIIIIIIIIII <3",
        "I CAN'T WAIT TO GET A WORKOUT IN WITH YOU <3",
        "LETS DO THIS !!! :)"
    ]
    message_index = 0
    space_press_count = 0  # Count number of space presses
    
    # Add your animation frames here
    lu_frames = [LUSTANDING1, LUSTANDING2]  # Replace with your actual frame surfaces
    
    rect_x, rect_y, rect_w, rect_h = 110, 544, 600, 128
    
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
    
        # Pick the current lu frame based on space_press_count // 2
        current_frame_index = min(space_press_count // 2, len(lu_frames) - 1)
        screen.blit(lu_frames[current_frame_index], (0, 0))
    
        pygame.draw.rect(screen, (118,66,138), (rect_x, rect_y, rect_w, rect_h))
    
        if message_index < len(messages):
            wrapped_lines = wrap_text(messages[message_index], font, rect_w - 10)
            for i, line in enumerate(wrapped_lines):
                line_surface = font.render(line, True, (0, 0, 0))
                screen.blit(line_surface, (rect_x + 5, rect_y + 5 + i * font.get_height()))
        else:
            pygame.mixer.music.stop()
            start_front_raise_pose(shared_camera, shared_mp_pose)
            pygame.mixer.music.load("Sounds/MENU.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            global victorycounter
            victorycounter += 1
            print(victorycounter)
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

def military_press_cutscene():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("Sounds/Military.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    font = pygame.font.Font("Fonts/pictochat.otf", 48)

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

    rect_x, rect_y, rect_w, rect_h = 110, 544, 600, 128

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
            pygame.mixer.music.load("Sounds/MENU.mp3")
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
    pygame.mixer.music.load("Sounds/red.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    global username

    font = pygame.font.Font("Fonts/pictochat.otf", 48)
    small_font = pygame.font.Font("Fonts/pictochat.otf", 24)  

    messages = [
        "You must be the new guy I've been hearing about!?",
        "Say new guy, you think you have what it takes to hit 8 perfect reps?",
    ]

    message_index = 0
    space_press_count = 0

    red_frames = [REDSTANDING1, REDSTANDING2]
    rect_x, rect_y, rect_w, rect_h = 110, 544, 600, 128

    input_text = ""
    input_rect = pygame.Rect(rect_x + 10, rect_y + 60, 580, 50)
    input_color = pygame.Color("white")

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
        screen.fill((0, 0, 0))
        current_frame_index = min(space_press_count // 2, len(red_frames) - 1)
        screen.blit(red_frames[current_frame_index], (0, 0))

        pygame.draw.rect(screen, (172, 50, 50), (rect_x, rect_y, rect_w, rect_h))

        if message_index < len(messages):  # Phase 0: Intro lines
            wrapped_lines = wrap_text(messages[message_index], font, rect_w - 10)
            for i, line in enumerate(wrapped_lines):
                line_surface = font.render(line, True, (0, 0, 0))
                screen.blit(line_surface, (rect_x + 5, rect_y + 5 + i * font.get_height()))
        elif message_index == len(messages):  # Phase 1: Ask for name
            # Character speaking
            question_surface = font.render("Say new guy, what's your name?", True, (0, 0, 0))
            screen.blit(question_surface, (rect_x + 5, rect_y + 5))

            # Prompt
            prompt_surface = small_font.render("Enter your name:", True, (255, 255, 255))
            screen.blit(prompt_surface, (input_rect.x, input_rect.y - 20))

            # Input box
            pygame.draw.rect(screen, input_color, input_rect, 2)
            text_surface = font.render(input_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        elif message_index == len(messages) + 1:  # Phase 2: Name acknowledgment
            greet = f"{username}, huh? Let's see what you got!"
            wrapped_lines = wrap_text(greet, font, rect_w - 10)
            for i, line in enumerate(wrapped_lines):
                line_surface = font.render(line, True, (0, 0, 0))
                screen.blit(line_surface, (rect_x + 5, rect_y + 5 + i * font.get_height()))
        elif message_index == len(messages) + 2:  # Phase 3: Final message
            final_msg = "Let's get it!"
            line_surface = font.render(final_msg, True, (0, 0, 0))
            screen.blit(line_surface, (rect_x + 5, rect_y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if message_index < len(messages):  # Advance intro lines
                    if event.key == pygame.K_SPACE:
                        message_index += 1
                        space_press_count += 1
                        pygame.mixer.Sound.set_volume(TEXT, 0.8)
                        pygame.mixer.Sound.play(TEXT)
                elif message_index == len(messages):  # Name input
                    if event.key == pygame.K_RETURN:
                        if input_text.strip():
                            username = input_text.strip()
                            message_index += 1  # Move to greeting
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 20:
                            input_text += event.unicode
                elif message_index == len(messages) + 1:  # Greet
                    if event.key == pygame.K_RETURN:
                        message_index += 1
                elif message_index == len(messages) + 2:  # Final "Let's get it!"
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        username = sanitize_username(username)
                        print(username)
                        start_bicep_curl_pose(shared_camera, shared_mp_pose)
                        pygame.mixer.music.load("Sounds/MENU.mp3")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                        return
                    
def start_bicep_curl_pose(camera, pose):
    pygame.mixer.music.load("Sounds/CAMERA.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    good_sound = pygame.mixer.Sound("Sounds/GOOD.mp3")
    bad_sound = pygame.mixer.Sound("Sounds/MISS.mp3")
    right_tip = ""
    left_tip = ""
    global goodrepright, goodrepleft, badrepleft, badrepright

    # camera = Camera()
    mp_pose = mp.solutions.pose
    # pose = pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Bicep Curl Tracker")

    font = pygame.font.Font("Fonts/pictochat.otf", 30)

    def draw_text(surface, text, pos, color=(255, 255, 255)):
        img = font.render(text, True, color)
        surface.blit(img, pos)

    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)

    right_counter, left_counter = 0, 0
    right_stage, left_stage = None, None
    right_feedback, left_feedback = "NEUTRAL", "NEUTRAL"
    right_angle, left_angle = 0, 0
    feedback_timer = 0

    camera_x, camera_y = 50, 50

    running = True
    while running:
        ret, frame = camera.cam.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Blank pose preview image
        pose_preview = np.zeros((480, 480, 3), dtype=np.uint8)

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            mp.solutions.drawing_utils.draw_landmarks(pose_preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            landmarks = results.pose_landmarks.landmark

            # Right arm
            r_shoulder = [landmarks[12].x, landmarks[12].y]
            r_elbow = [landmarks[14].x, landmarks[14].y]
            r_wrist = [landmarks[16].x, landmarks[16].y]
            right_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)

            # Right Arm Logic
            if right_angle > 160:
                right_stage = "down"
                
            if right_angle < 60 and right_stage == "down":
                right_stage = "up"
                # Only count as a GOOD rep if the angle is between 40 and 180
                if 40 <= right_angle <= 180:
                    right_counter += 1
                    right_feedback = "GOOD"
                    goodrepright += 1
                    good_sound.play()
                    right_tip = ""  # Clear any previous hint when a GOOD rep happens
                else:
                    right_feedback = "BAD"
                    badrepright += 1
                    bad_sound.play()
                    # Give feedback tips if BAD rep (only when feedback is BAD)
                    if right_angle > 130:
                        right_tip = "Lower your arm more!"
                    elif right_angle < 70:
                        right_current_angle = int(right_angle)
                        right_tip = (f"Curl higher! {right_current_angle}")
                    else:
                        right_tip = ""
                feedback_timer = pygame.time.get_ticks()

            # Left arm
            l_shoulder = [landmarks[11].x, landmarks[11].y]
            l_elbow = [landmarks[13].x, landmarks[13].y]
            l_wrist = [landmarks[15].x, landmarks[15].y]
            left_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)

            if left_angle > 160:
                left_stage = "down"
                
            if left_angle < 60 and left_stage == "down":
                left_stage = "up"
                if 40 <= left_angle <= 180:
                    left_counter += 1
                    left_feedback = "GOOD"
                    goodrepleft += 1
                    good_sound.play()
                    left_tip = ""  # Clear previous hint on GOOD rep
                else:
                    left_feedback = "BAD"
                    badrepleft += 1
                    bad_sound.play()
                    # Provide feedback tips for BAD rep
                    if left_angle > 130:
                        left_tip = "Lower your arm more!"
                    elif left_angle < 70:
                        left_current_angle = int(left_angle)
                        left_tip = (f"Curl higher! {left_current_angle}")
                    else:
                        left_tip = ""
                feedback_timer = pygame.time.get_ticks()

            # Color lines based on good/bad angle
            if 40 <= right_angle <= 180:
                right_color = (0, 255, 0)  # Green for good
            else:
                right_color = (255, 0, 0)  # Red for bad

            if 40 <= left_angle <= 180:
                left_color = (0, 255, 0)  # Green for good
            else:
                left_color = (255, 0, 0)  # Red for bad

            # Draw lines between shoulder, elbow, and wrist for both arms
            cv2.line(frame, (int(r_shoulder[0] * frame.shape[1]), int(r_shoulder[1] * frame.shape[0])), 
                     (int(r_elbow[0] * frame.shape[1]), int(r_elbow[1] * frame.shape[0])), right_color, 5)
            cv2.line(frame, (int(r_elbow[0] * frame.shape[1]), int(r_elbow[1] * frame.shape[0])), 
                     (int(r_wrist[0] * frame.shape[1]), int(r_wrist[1] * frame.shape[0])), right_color, 5)

            cv2.line(frame, (int(l_shoulder[0] * frame.shape[1]), int(l_shoulder[1] * frame.shape[0])), 
                     (int(l_elbow[0] * frame.shape[1]), int(l_elbow[1] * frame.shape[0])), left_color, 5)
            cv2.line(frame, (int(l_elbow[0] * frame.shape[1]), int(l_elbow[1] * frame.shape[0])), 
                     (int(l_wrist[0] * frame.shape[1]), int(l_wrist[1] * frame.shape[0])), left_color, 5)

        # Feedback color
        elapsed = pygame.time.get_ticks() - feedback_timer
        if elapsed > 1500:
            feedback_color = (100, 100, 100)
            right_feedback, left_feedback = "NEUTRAL", "NEUTRAL"
        elif right_feedback == "BAD" or left_feedback == "BAD":
            feedback_color = (255, 0, 0)
        elif right_feedback == "GOOD" or left_feedback == "GOOD":
            feedback_color = (0, 255, 0)
        else:
            feedback_color = (100, 100, 100)

        # Convert camera feed
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = np.rot90(frame_rgb)
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        frame_surface = pygame.transform.scale(frame_surface, (480, 360))

        # Convert pose preview
        preview_rgb = cv2.cvtColor(pose_preview, cv2.COLOR_BGR2RGB)
        preview_rgb = np.rot90(preview_rgb)
        preview_surface = pygame.surfarray.make_surface(preview_rgb)
        preview_surface = pygame.transform.scale(preview_surface, (200, 150))

        screen.fill((172,50,50))  

        # Draw camera preview
        screen.blit(frame_surface, (camera_x, camera_y))

        # Border highlight
        border_rect = pygame.Rect(camera_x - 5, camera_y - 5, 490, 370)
        pygame.draw.rect(screen, feedback_color, border_rect, 5)

        # Pose preview (to the left of camera)
        screen.blit(preview_surface, (camera_x + 520, camera_y ))

        # Right Arm Text
        draw_text(screen, f"Left Arm Reps: {left_counter}", (camera_x, camera_y + 410))
        draw_text(screen, f"Left Angle: {int(left_angle)}°", (camera_x, camera_y + 370))
        draw_text(screen, f"{left_feedback} REP", (camera_x, camera_y + 450),
                  (0, 255, 0) if left_feedback == "GOOD" else (255, 0, 0) if left_feedback == "BAD" else (255, 255, 255))
        
        # Left Arm Text
        draw_text(screen, f"Right Arm Reps: {right_counter}", (camera_x + 250, camera_y + 410))
        draw_text(screen, f"Right Angle: {int(right_angle)}°", (camera_x + 250, camera_y + 370))
        draw_text(screen, f"{right_feedback} REP", (camera_x + 250, camera_y + 450),
                  (0, 255, 0) if right_feedback == "GOOD" else (255, 0, 0) if right_feedback == "BAD" else (255, 255, 255))

        # draw_text(screen, "ESC to exit", (50, 550))
        draw_text(screen, right_tip, (camera_x + 250, camera_y + 500), (255, 255, 0))
        draw_text(screen, left_tip, (camera_x, camera_y + 500), (255, 255, 0))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            screen = pygame.display.set_mode((800, 800))
            submit_score(username, goodrepright, badrepright, goodrepleft, badrepleft)
            goodrepright = 0
            badrepright = 0
            goodrepleft = 0
            badrepleft = 0
            return

def start_front_raise_pose(camera, pose):
    pygame.mixer.music.load("CAMERA.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    good_sound = pygame.mixer.Sound("GOOD.mp3")
    bad_sound = pygame.mixer.Sound("MISS.mp3")
    right_angle = 0
    left_angle = 0
    right_tip = ""
    left_tip = ""
    last_right_feedback = "NEUTRAL"
    last_left_feedback = "NEUTRAL"
    right_hold_start_time = 0
    left_hold_start_time = 0
    COOLDOWN_DURATION = 2500  # milliseconds
    right_cooldown = 0
    left_cooldown = 0


    mp_pose = mp.solutions.pose
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Front Raise Tracker")
    font = pygame.font.Font("pictochat.otf", 30)

    def draw_text(surface, text, pos, color=(255, 255, 255)):
        img = font.render(text, True, color)
        surface.blit(img, pos)

    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)

    right_counter, left_counter = 0, 0
    right_stage, left_stage = None, None
    right_feedback, left_feedback = "NEUTRAL", "NEUTRAL"
    camera_x, camera_y = 50, 50
    feedback_timer = 0

    running = True
    while running:
        ret, frame = camera.cam.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)
        pose_preview = np.zeros((480, 480, 3), dtype=np.uint8)

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            mp.solutions.drawing_utils.draw_landmarks(pose_preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            lm = results.pose_landmarks.landmark

            # Use hip-shoulder-wrist for front raise angle
            r_hip = [lm[24].x, lm[24].y]
            r_shoulder = [lm[12].x, lm[12].y]
            r_wrist = [lm[16].x, lm[16].y]
            right_angle = calculate_angle(r_hip, r_shoulder, r_wrist)

            if right_angle < 30:
                if right_stage != "down":
                    right_stage = "down"
            
            # Rep completes when arm goes up *after being down*
            if right_angle > 80 and right_stage == "down":
                if right_hold_start_time == 0:
                    right_hold_start_time = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - right_hold_start_time > 500:
                    right_stage = "up"
                    right_counter += 1
                    right_feedback = "GOOD"
                    good_sound.play()
                    right_cooldown = pygame.time.get_ticks()
            else:
                right_hold_start_time = 0  # reset if angle not held
            

            # Repeat for left arm
            l_hip = [lm[23].x, lm[23].y]
            l_shoulder = [lm[11].x, lm[11].y]
            l_wrist = [lm[15].x, lm[15].y]
            left_angle = calculate_angle(l_hip, l_shoulder, l_wrist)

            if left_angle < 30:
                if left_stage != "down":
                    left_stage = "down"
            
            if left_angle > 80 and left_stage == "down":
                left_stage = "up"
                left_counter += 1
                left_feedback = "GOOD"
                good_sound.play()
                feedback_timer = pygame.time.get_ticks()
                left_cooldown = pygame.time.get_ticks() 
            
            # --- RIGHT ARM FORM CHECK ---
            if right_stage == "up" and pygame.time.get_ticks() - right_cooldown > COOLDOWN_DURATION:
                if not (80 <= right_angle <= 120) or abs(r_wrist[0] - r_shoulder[0]) > 0.2 or r_wrist[1] > r_shoulder[1]:
                    if right_feedback != "BAD":
                        bad_sound.play()
                    right_feedback = "BAD"
                    if right_angle < 70:
                        right_tip = "Raise higher!"
                    elif right_angle > 120:
                        right_tip = "Too high!"
                    elif abs(r_wrist[0] - r_shoulder[0]) > 0.2:
                        right_tip = "Keep arm in front!"
                    elif r_wrist[1] > r_shoulder[1]:
                        right_tip = "Wrist not above shoulder!"
                else:
                    if right_feedback != "GOOD":
                        good_sound.play()
                    right_feedback = "GOOD"
                    right_tip = ""
            
            # ---- LEFT ARM FORM CHECK ----
            if left_stage == "up" and pygame.time.get_ticks() - left_cooldown > COOLDOWN_DURATION:
                if not (80 <= left_angle <= 120) or abs(l_wrist[0] - l_shoulder[0]) > 0.2 or l_wrist[1] > l_shoulder[1]:
                    if left_feedback != "BAD":
                        bad_sound.play()
                    left_feedback = "BAD"
                    if left_angle < 70:
                        left_tip = "Raise higher!"
                    elif left_angle > 120:
                        left_tip = "Too high!"
                    elif abs(l_wrist[0] - l_shoulder[0]) > 0.2:
                        left_tip = "Keep arm in front!"
                    elif l_wrist[1] > l_shoulder[1]:
                        left_tip = "Wrist not above shoulder!"
                else:
                    if left_feedback != "GOOD":
                        good_sound.play()
                    left_feedback = "GOOD"
                    left_tip = ""

        elapsed = pygame.time.get_ticks() - feedback_timer
        feedback_color = (0, 255, 0) if elapsed < 1500 else (100, 100, 100)
        right_color = (0, 255, 0) if right_feedback == "GOOD" else (255, 0, 0) if right_feedback == "BAD" else (200, 200, 200)
        left_color = (0, 255, 0) if left_feedback == "GOOD" else (255, 0, 0) if left_feedback == "BAD" else (200, 200, 200)
        

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = np.rot90(frame_rgb)
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        frame_surface = pygame.transform.scale(frame_surface, (480, 360))

        preview_rgb = cv2.cvtColor(pose_preview, cv2.COLOR_BGR2RGB)
        preview_rgb = np.rot90(preview_rgb)
        preview_surface = pygame.surfarray.make_surface(preview_rgb)
        preview_surface = pygame.transform.scale(preview_surface, (200, 150))

        screen.fill((118,66,138))
        screen.blit(frame_surface, (camera_x, camera_y))
        pygame.draw.rect(screen, feedback_color, pygame.Rect(camera_x - 5, camera_y - 5, 490, 370), 5)
        screen.blit(preview_surface, (camera_x + 520, camera_y))

        # Right arm text
        draw_text(screen, f"Right Angle: {int(right_angle)}°", (camera_x, camera_y + 370))
        draw_text(screen, f"Right Arm Reps: {right_counter}", (camera_x, camera_y + 410))
        draw_text(screen, f"{right_feedback}", (camera_x, camera_y + 450), right_color)
        draw_text(screen, right_tip, (camera_x, camera_y + 500), (255, 255, 0))
        
        # Left arm text
        draw_text(screen, f"Left Angle: {int(left_angle)}°", (camera_x + 250, camera_y + 370))
        draw_text(screen, f"Left Arm Reps: {left_counter}", (camera_x + 250, camera_y + 410))
        draw_text(screen, f"{left_feedback}", (camera_x + 250, camera_y + 450), left_color)
        draw_text(screen, left_tip, (camera_x + 250, camera_y + 500), (255, 255, 0))
        

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            screen = pygame.display.set_mode((800, 800))
            return

def finalboss():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("girl.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    font = pygame.font.SysFont(None, 36)
    message = "FINAL BOSS TIME!"

    while True:
        screen.fill((0, 0, 0))
        logo_x = (800 - LOGO.get_width()) // 2
        logo_y = (800 - LOGO.get_height()) // 2
        screen.blit(LOGO, (logo_x, logo_y))

        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 700))
        screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # or launch a new boss gameplay mode

def show_loading_screen(message="Loading camera and pose model..."):
    screen.fill((0, 0, 0))
    font = pygame.font.Font("Fonts/pictochat.otf", 40)
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()


show_start_menu()
show_loading_screen()

try:
    shared_camera = Camera()
except Exception as e:
    print("Camera failed to open:", e)
    pygame.quit()
    exit()

shared_mp_pose = mp.solutions.pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
# start_front_raise_pose(shared_camera, shared_mp_pose)

pygame.mixer.music.load("Sounds/MENU.mp3")
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
        # military_press_cutscene()

    if front_button.draw(screen):
        print("FrontRaise")
        pygame.mixer.Sound.play(OPENSOUND)
        # front_raise_curscene()

    # if victorycounter == 3:
    #     finalboss()

    # flip() the display to put your work on screen
    logo_x = (800 - LOGO.get_width()) // 2
    screen.blit(LOGO, (logo_x, 0))
    
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()