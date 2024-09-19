import pygame
import time

# Set display surface
pygame.init()
pygame.mixer.init()

# Set display surface
WINDOW_WIDTH = 816
WINDOW_HEIGHT = 736
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MEOW")

# Colors
BLACK = (0, 0, 0)

pygame.mixer.music.load('assets/Cat_Meow.wav')

# Load the image
player_image = pygame.image.load("assets/Cat.jpg")  # Load the image

# Scale the image up (e.g., double the size)
scaled_image = pygame.transform.smoothscale(player_image, (816, 736))  # New width and height

# Get the scaled image's rectangle
player_rect = scaled_image.get_rect()

# Set the rectangle to be centered in the window
player_rect.centerx = WINDOW_WIDTH // 2  # Center horizontally
player_rect.centery = WINDOW_HEIGHT // 2  # Center vertically


# The main game loop
running = True
while running:
    # Check for user input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Fill the display
        display_surface.fill(BLACK)

        # Blit the scaled image
        display_surface.blit(scaled_image, player_rect)

        # Update the display
        pygame.display.update()  # <- This updates the screen to show the image

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
         pygame.mixer.music.play(1, 0.0)

pygame.quit()