import cv2
import pygame
import mediapipe as mp
import numpy as np

# Initialize Pygame
pygame.init()

# Capture video from webcam
cap = cv2.VideoCapture(0)
width, height = int(cap.get(3)), int(cap.get(4))  # Get webcam resolution

# Create a Pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("FORM-AI")

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Load and scale overlay images
image_parappa_load = pygame.image.load("PaRappa.png") 
image_down_load = pygame.image.load("down2.png")
image_up_load = pygame.image.load("up.png")
scaled_image = pygame.transform.scale(image_parappa_load, (200, 200))
scaled_up = pygame.transform.scale(image_up_load, (100, 100))
scaled_down = pygame.transform.scale(image_down_load, (100, 100))

# Curl detection variables
bicep_curl_count = 0
arm_fully_extended = True  # Track if the arm is extended
show_arrow = None  # Track which arrow to show

def calculate_angle(a, b, c):
    """Calculate angle between three points using the dot product formula"""
    a = np.array(a)  # Shoulder
    b = np.array(b)  # Elbow
    c = np.array(c)  # Wrist

    ab = a - b
    cb = c - b

    cosine_angle = np.dot(ab, cb) / (np.linalg.norm(ab) * np.linalg.norm(cb))
    angle = np.arccos(cosine_angle)  # Get angle in radians
    return np.degrees(angle)  # Convert to degrees

running = True
while running and cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert to RGB for Mediapipe processing
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and detect poses
    results = pose.process(image)

    # Convert back to BGR for OpenCV processing
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Reset arrow display
    show_arrow = None  

    # Draw pose landmarks
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Extract keypoints
        landmarks = results.pose_landmarks.landmark
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * width, 
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * height]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * width, 
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * height]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x * width, 
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y * height]

        # Calculate the elbow angle
        angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

        # Check for a bicep curl and update arrow display
        if angle > 160:  # Arm is fully extended
            arm_fully_extended = True
            show_arrow = "up"
        if arm_fully_extended and angle < 60:  # Arm is fully bent (curl completed)
            bicep_curl_count += 1
            show_arrow = "down"
            arm_fully_extended = False  # Prevent multiple counts per curl

        # Display the angle and count on the image
        cv2.putText(image, f'Angle: {int(angle)}', (50, 50), 
                    cv2.FONT_ITALIC, 1, (0, 255, 0), 2)
        cv2.putText(image, f'Curls: {bicep_curl_count}', (50, 100), 
                    cv2.FONT_ITALIC, 1, (0, 255, 0), 2)

    # Convert image to Pygame surface
    image = cv2.flip(image, 1)  # Flip for a mirror effect
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Fix colors for Pygame
    frame_surface = pygame.surfarray.make_surface(cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE))

    # # Display image in Pygame window
    screen.blit(frame_surface, (0, 0))
    # screen.blit(scaled_image, (300, 0))  # Overlay character image

    # # Display arrow in the center of the screen
    # if show_arrow == "up":
    #     screen.blit(scaled_up, (width // 2 - 50, height // 2 - 200))  # Position the UP arrow
    # elif show_arrow == "down":
    #     screen.blit(scaled_down, (width // 2 - 50, height // 2 + 100))  # Position the DOWN arrow

    pygame.display.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False

# Release resources
cap.release()
pygame.quit()
