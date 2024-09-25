import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set display surface
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MEOW - 2 Player Mode")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
FOOD_STARTING_VELOCITY = 5
FOOD_ACCELERATION = 0.05
BUFFER_DISTANCE = 100
MOUTH_OPEN_DURATION = 200  # Duration the mouth stays open in milliseconds
SCRATCH_IMAGE_PATH = "assets/CatScratch.png"

# File path for high score
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    """Load the high score from a file."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                score = int(file.read().strip())
                return score
        except ValueError:
            return 0
    return 0

def save_high_score(score):
    """Save the high score to a file."""
    try:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))
    except IOError:
        print("Error saving high score.")

# Load the initial high score
high_score = load_high_score()

# Set Game Variables
score_p1 = 0
score_p2 = 0
player_lives_p1 = PLAYER_STARTING_LIVES
player_lives_p2 = PLAYER_STARTING_LIVES
food_velocity = FOOD_STARTING_VELOCITY
mouth_open_time_p1 = 0  # Time to keep the mouth open for player 1
mouth_open_time_p2 = 0  # Time to keep the mouth open for player 2
paused = False  # Pause state

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (178, 238, 240)
PURPLE = (200, 102, 227)
DARK_PURPLE = (132, 45, 158)

# Set fonts
font = pygame.font.Font('assets/HappyParadise.otf', 32)

# Set Text for Score
score_text_p1 = font.render("Player 1 Score: " + str(score_p1), True, PURPLE, DARK_PURPLE)
score_text_p2 = font.render("Player 2 Score: " + str(score_p2), True, PURPLE, DARK_PURPLE)
score_rect_p1 = score_text_p1.get_rect(topleft=(10, 10))
score_rect_p2 = score_text_p2.get_rect(topright=(WINDOW_WIDTH - 10, 10))

# Set Text for High Score
high_score_text = font.render("High Score: " + str(high_score), True, PURPLE, DARK_PURPLE)
high_score_rect = high_score_text.get_rect()
high_score_rect.centerx = WINDOW_WIDTH // 2
high_score_rect.y = 10

# Set Text for Lives
lives_text_p1 = font.render("Lives: " + str(player_lives_p1), True, PURPLE, DARK_PURPLE)
lives_text_p2 = font.render("Lives: " + str(player_lives_p2), True, PURPLE, DARK_PURPLE)
lives_rect_p1 = lives_text_p1.get_rect(topleft=(10, 50))
lives_rect_p2 = lives_text_p2.get_rect(topright=(WINDOW_WIDTH - 10, 50))

# Set Text for Game Over
game_over_text = font.render("GAME OVER", True, PURPLE, DARK_PURPLE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# Set Text for Continue
continue_text = font.render("Press any key to play again", True, PURPLE, DARK_PURPLE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 32)

# Set Text for Paused
paused_text = font.render("PAUSED", True, PURPLE, DARK_PURPLE)
paused_rect = paused_text.get_rect()
paused_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# Set the sound and music
food_sound = pygame.mixer.Sound('assets/Cat_Meow.wav')
miss_sound = pygame.mixer.Sound('assets/Cat_Hiss.wav')
miss_sound.set_volume(0.5)
pygame.mixer.music.load('assets/ftd_background_music.wav')

# Load the images
player_image_p1 = pygame.image.load("assets/Cat.mouth.closed.left.png")  # Left-facing cat for Player 1
player_image_p2 = pygame.image.load("assets/Cat.mouth.closed.right.png")  # Right-facing cat for Player 2

# Scale the images
scaled_image_p1 = pygame.transform.scale(player_image_p1, (57.86, 62.42))
scaled_image_p2 = pygame.transform.scale(player_image_p2, (57.86, 62.42))

# Initialize player_rect with the scaled images
player_rect_p1 = scaled_image_p1.get_rect(center=(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2))
player_rect_p2 = scaled_image_p2.get_rect(center=(WINDOW_WIDTH // 2 + 200, WINDOW_HEIGHT // 2))

# Load and scale food images
food_image_p1 = pygame.image.load("assets/Food.png")
food_image_p2 = pygame.image.load("assets/Food.png")
scaled_food_p1 = pygame.transform.scale(food_image_p1, (57.86, 62.42))
scaled_food_p2 = pygame.transform.scale(food_image_p2, (57.86, 62.42))

# Initialize food positions off-screen
food_rect_p1 = scaled_food_p1.get_rect(center=(0, random.randint(100, WINDOW_HEIGHT - 100)))  # Start off-screen to the left
food_rect_p2 = scaled_food_p2.get_rect(center=(WINDOW_WIDTH, random.randint(100, WINDOW_HEIGHT - 100)))  # Start off-screen to the right

# Load the scratch image
scratch_image = pygame.image.load(SCRATCH_IMAGE_PATH)
scratch_image = pygame.transform.scale(scratch_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
scratch_rect = scratch_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

# Start background music
pygame.mixer.music.play(-1, 0.0)

# Function to reset food position for Player 1
def reset_food_p1():
    food_rect_p1.centerx = WINDOW_WIDTH // 2
    food_rect_p1.centery = random.randint(64, WINDOW_HEIGHT - 32)

# Function to reset food position for Player 2
def reset_food_p2():
    food_rect_p2.centerx = WINDOW_WIDTH // 2
    food_rect_p2.centery = random.randint(64, WINDOW_HEIGHT - 32)

# The main game loop
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if paused:
                    paused = False
                    pygame.mixer.music.unpause()
                else:
                    paused = True
                    pygame.mixer.music.pause()

    if not paused:
        # Player 1 controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_rect_p1.top > 90:
            player_rect_p1.y -= PLAYER_VELOCITY
        if keys[pygame.K_s] and player_rect_p1.bottom < WINDOW_HEIGHT:
            player_rect_p1.y += PLAYER_VELOCITY

        # Player 2 controls
        if keys[pygame.K_UP] and player_rect_p2.top > 90:
            player_rect_p2.y -= PLAYER_VELOCITY
        if keys[pygame.K_DOWN] and player_rect_p2.bottom < WINDOW_HEIGHT:
            player_rect_p2.y += PLAYER_VELOCITY

        # Move the food towards each player
        food_rect_p1.x -= food_velocity
        food_rect_p2.x += food_velocity

        # Check if the food goes off the screen (missed food)
        if food_rect_p1.x < 0:
            miss_sound.play()
            player_lives_p1 -= 1
            reset_food_p1()

        if food_rect_p2.x > WINDOW_WIDTH:
            miss_sound.play()
            player_lives_p2 -= 1
            reset_food_p2()

        # Check for collision with the food for Player 1
        if player_rect_p1.colliderect(food_rect_p1):
            food_sound.play()
            score_p1 += 1
            reset_food_p1()
            food_velocity += FOOD_ACCELERATION

        # Check for collision with the food for Player 2
        if player_rect_p2.colliderect(food_rect_p2):
            food_sound.play()
            score_p2 += 1
            reset_food_p2()
            food_velocity += FOOD_ACCELERATION

        # Update text
        score_text_p1 = font.render("Player 1 Score: " + str(score_p1), True, PURPLE, DARK_PURPLE)
        score_text_p2 = font.render("Player 2 Score: " + str(score_p2), True, PURPLE, DARK_PURPLE)
        lives_text_p1 = font.render("Lives: " + str(player_lives_p1), True, PURPLE, DARK_PURPLE)
        lives_text_p2 = font.render("Lives: " + str(player_lives_p2), True, PURPLE, DARK_PURPLE)

        # Fill the display
        display_surface.fill(LIGHT_BLUE)

        # Draw the separator line
        pygame.draw.line(display_surface, DARK_PURPLE, (0, 100), (WINDOW_WIDTH, 100), 5)

        # Blit text and images
        display_surface.blit(score_text_p1, score_rect_p1)
        display_surface.blit(score_text_p2, score_rect_p2)
        display_surface.blit(high_score_text, high_score_rect)
        display_surface.blit(lives_text_p1, lives_rect_p1)
        display_surface.blit(lives_text_p2, lives_rect_p2)
        display_surface.blit(scaled_image_p1, player_rect_p1)
        display_surface.blit(scaled_image_p2, player_rect_p2)
        display_surface.blit(scaled_food_p1, food_rect_p1)
        display_surface.blit(scaled_food_p2, food_rect_p2)

        # Check for game over for both players
        if player_lives_p1 <= 0 or player_lives_p2 <= 0:
            display_surface.blit(scratch_image, scratch_rect)
            display_surface.blit(game_over_text, game_over_rect)
            display_surface.blit(continue_text, continue_rect)
            pygame.display.update()

            save_high_score(max(score_p1, score_p2))

            waiting_for_key = True
            while waiting_for_key:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_key = False
                    if event.type == pygame.KEYDOWN:
                        score_p1 = 0
                        score_p2 = 0
                        player_lives_p1 = PLAYER_STARTING_LIVES
                        player_lives_p2 = PLAYER_STARTING_LIVES
                        food_velocity = FOOD_STARTING_VELOCITY
                        player_rect_p1 = scaled_image_p1.get_rect(left=32, centery=WINDOW_HEIGHT // 2)
                        player_rect_p2 = scaled_image_p2.get_rect(right=WINDOW_WIDTH - 32, centery=WINDOW_HEIGHT // 2)
                        reset_food_p1()
                        reset_food_p2()
                        pygame.mixer.music.play(-1, 0.0)
                        waiting_for_key = False

        # Display everything
        pygame.display.update()
        clock.tick(FPS)
    else:
        display_surface.blit(paused_text, paused_rect)
        pygame.display.update()

# Quit Pygame
pygame.quit()