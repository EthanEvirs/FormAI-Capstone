import pygame
pygame.mixer.init()
selection = pygame.mixer.Sound("button.wav")

class Button:
    def __init__(self, x, y, image, scale, hover_image=None):
        """
        Button class to handle image changes on hover and mouse clicks.
        :param x, y: Position of the button
        :param image: Default button image
        :param scale: Scale factor to resize the button
        :param hover_image: Optional image for the hover state (default is None)
        """
        self.default_image = pygame.transform.scale(
            image, (int(image.get_width() * scale), int(image.get_height() * scale))
        )

        self.hover_image = hover_image
        if hover_image:
            self.hover_image = pygame.transform.scale(
                hover_image, (int(hover_image.get_width() * scale), int(hover_image.get_height() * scale))
            )

        # Set the initial image as default
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.sound_played = False

    def draw(self, surface):
        """
        Draws the button on the screen and checks for hover/click interactions.
        :param surface: The surface to draw the button on
        :return: Boolean indicating if the button was clicked
        """
        action = False
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the button (hover effect)
        if self.rect.collidepoint(pos):
            if self.hover_image:  # Only change image if hover image is provided
                self.image = self.hover_image
            if not self.sound_played:
                pygame.mixer.Sound.play(selection)
                self.sound_played = True
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.image = self.default_image  # Reset to default image when not hovered
            self.sound_played = False

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        # Draw the button on the surface
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
