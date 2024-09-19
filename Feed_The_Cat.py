import pygame
import random
import os  # To handle saving and loading high score from a file

# Initialize Pygame
pygame.init()

# Set display surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("MEOW")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
FOOD_STARTING_VELOCITY = 10
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
                print(f"High score loaded: {score}")  # Debug statement
                return score
        except ValueError:
            print("Error reading high score. Resetting to 0.")  # Debug statement
            return 0
    return 0

def save_high_score(score):
    """Save the high score to a file."""
    try:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))
            print(f"High score saved: {score}")  # Debug statement
    except IOError:
        print("Error saving high score.")  # Debug statement

# Load the initial high score
high_score = load_high_score()

# Set Game Variables
score = 0
player_lives = PLAYER_STARTING_LIVES
food_velocity = FOOD_STARTING_VELOCITY
mouth_open_time = 0  # Time to keep the mouth open
show_scratch = False  # Whether to show the scratch effect
player_image = None  # To track current player image
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
score_text = font.render("Score: " + str(score), True, PURPLE, DARK_PURPLE)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

# Set text for highscore
high_score_text = font.render("High Score: " + str(high_score), True, PURPLE, DARK_PURPLE)
high_score_rect = high_score_text.get_rect()
high_score_rect.topleft = (10, 50)  # Below the score

# Set Text for Title
title_text = font.render("Feed the Cat: ", True, PURPLE, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH // 2
title_rect.y = 10

# Set Text for Lives
lives_text = font.render("Lives: " + str(player_lives), True, PURPLE, DARK_PURPLE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

# Set Text for Game Over
game_over_text = font.render("GAMEOVER", True, PURPLE, DARK_PURPLE)
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
miss_sound.set_volume(0.5)  # Increase volume for testing
pygame.mixer.music.load('assets/ftd_background_music.wav')

# Load the images
player_image_closed = pygame.image.load("assets/Cat.mouth.closed.png")
player_image_open = pygame.image.load("assets/Cat.mouth.open.png")

# Scale the images
scaled_image_closed = pygame.transform.scale(player_image_closed, (57.86, 62.42))
scaled_image_open = pygame.transform.scale(player_image_open, (57.86, 62.42))

# Initialize player_rect with the closed-mouth image
player_rect = scaled_image_closed.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT // 2

# Load and scale food image
food_image = pygame.image.load("assets/Food.png")
scaled_food = pygame.transform.scale(food_image, (57.86, 62.42))
food_rect = scaled_food.get_rect()
food_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
food_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

# Load the scratch image
scratch_image = pygame.image.load(SCRATCH_IMAGE_PATH)
scratch_image = pygame.transform.scale(scratch_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Scale to final size
scratch_rect = scratch_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

# Start background music
pygame.mixer.music.play(-1, 0.0)

# Function to reset food position
def reset_food():
    food_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
    food_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

# The main game loop
running = True
while running:
    import pygame
    import random
    import os  # To handle saving and loading high score from a file

    # Initialize Pygame
    pygame.init()

    # Set display surface
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 400
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("MEOW")

    # Set FPS and clock
    FPS = 60
    clock = pygame.time.Clock()

    # Set game values
    PLAYER_STARTING_LIVES = 5
    PLAYER_VELOCITY = 10
    FOOD_STARTING_VELOCITY = 10
    FOOD_ACCELERATION = 0.5
    BUFFER_DISTANCE = 100
    MOUTH_OPEN_DURATION = 200  # Duration the mouth stays open in milliseconds
    SCRATCH_ZOOM_DURATION = 1000  # Duration for the scratch to grow (in milliseconds)
    MAX_SCRATCH_SCALE = 2  # Maximum scale for the scratch effect

    # File path for high score
    HIGH_SCORE_FILE = "highscore.txt"


    def load_high_score():
        """Load the high score from a file."""
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, "r") as file:
                    score = int(file.read().strip())
                    print(f"High score loaded: {score}")  # Debug statement
                    return score
            except ValueError:
                print("Error reading high score. Resetting to 0.")  # Debug statement
                return 0
        return 0


    def save_high_score(score):
        """Save the high score to a file."""
        try:
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(score))
                print(f"High score saved: {score}")  # Debug statement
        except IOError:
            print("Error saving high score.")  # Debug statement


    high_score = load_high_score()

    # Set Game Variables
    score = 0
    player_lives = PLAYER_STARTING_LIVES
    food_velocity = FOOD_STARTING_VELOCITY
    mouth_open_time = 0  # Time to keep the mouth open
    scratch_start_time = 0  # Time when the scratch effect starts
    show_scratch = False  # Whether to show the scratch effect
    player_image = None  # To track current player image
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
    score_text = font.render("Score: " + str(score), True, PURPLE, DARK_PURPLE)
    score_rect = score_text.get_rect()
    score_rect.topleft = (10, 10)

    # Set text for highscore
    high_score_text = font.render("High Score: " + str(high_score), True, PURPLE, DARK_PURPLE)
    high_score_rect = high_score_text.get_rect()
    high_score_rect.topleft = (10, 50)  # Below the score

    # Set Text for Title
    title_text = font.render("Feed the Cat: ", True, PURPLE, WHITE)
    title_rect = title_text.get_rect()
    title_rect.centerx = WINDOW_WIDTH // 2
    title_rect.y = 10

    # Set Text for Lives
    lives_text = font.render("Lives: " + str(player_lives), True, PURPLE, DARK_PURPLE)
    lives_rect = lives_text.get_rect()
    lives_rect.topright = (WINDOW_WIDTH - 10, 10)

    # Set Text for Game Over
    game_over_text = font.render("GAMEOVER", True, PURPLE, DARK_PURPLE)
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
    miss_sound.set_volume(0.5)  # Increase volume for testing
    pygame.mixer.music.load('assets/ftd_background_music.wav')

    # Load the images
    player_image_closed = pygame.image.load("assets/Cat.mouth.closed.png")
    player_image_open = pygame.image.load("assets/Cat.mouth.open.png")

    # Scale the images
    scaled_image_closed = pygame.transform.scale(player_image_closed, (57.86, 62.42))
    scaled_image_open = pygame.transform.scale(player_image_open, (57.86, 62.42))

    # Initialize player_rect with the closed-mouth image
    player_rect = scaled_image_closed.get_rect()
    player_rect.left = 32
    player_rect.centery = WINDOW_HEIGHT // 2

    # Load and scale food image
    food_image = pygame.image.load("assets/Food.png")
    scaled_food = pygame.transform.scale(food_image, (57.86, 62.42))
    food_rect = scaled_food.get_rect()
    food_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
    food_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

    # Load the scratch image
    scratch_image = pygame.image.load("assets/CatScratch.png")
    scratch_image = pygame.transform.scale(scratch_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Start at screen size
    scratch_rect = scratch_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    # Start background music
    pygame.mixer.music.play(-1, 0.0)


    # Function to reset food position
    def reset_food():
        food_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        food_rect.y = random.randint(64, WINDOW_HEIGHT - 32)


    # The main game loop
    running = True
    while running:
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

        # Check for user input/events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle pause input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if paused:
                        paused = False
                        pygame.mixer.music.unpause()  # Resume the music when game is unpaused
                    else:
                        paused = True
                        pygame.mixer.music.pause()  # Pause the music when game is paused

        if not paused:
            # Move the player (Cat movement logic)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and player_rect.top > 90:
                player_rect.y -= PLAYER_VELOCITY
            if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
                player_rect.y += PLAYER_VELOCITY

            # Move the food
            food_rect.x -= food_velocity

            # Check if the food goes off the screen (missed food)
            if food_rect.x < 0:
                miss_sound.play()
                player_lives -= 1
                reset_food()

            # Check for collision with the food
            if player_rect.colliderect(food_rect):
                food_sound.play()
                score += 1
                if score > high_score:
                    high_score = score
                reset_food()
                food_velocity += FOOD_ACCELERATION
                player_image = scaled_image_open  # Change to the open-mouth image
                mouth_open_time = current_time  # Set the time when the mouth opens

            # Check if the mouth should be closed
            if current_time - mouth_open_time > MOUTH_OPEN_DURATION:
                player_image = scaled_image_closed  # Change back to the closed-mouth image

            score_text = font.render("Score: " + str(score), True, PURPLE, DARK_PURPLE)
            high_score_text = font.render("High Score: " + str(high_score), True, PURPLE, DARK_PURPLE)
            lives_text = font.render("Lives: " + str(player_lives), True, PURPLE, DARK_PURPLE)

            # Fill the display
            display_surface.fill(LIGHT_BLUE)

            # Blit text and images
            display_surface.blit(score_text, score_rect)
            display_surface.blit(high_score_text, high_score_rect)  # Display high score
            display_surface.blit(title_text, title_rect)
            display_surface.blit(lives_text, lives_rect)
            display_surface.blit(player_image, player_rect)
            display_surface.blit(scaled_food, food_rect)

            # Check for game over
            if player_lives <= 0:
                if not show_scratch:
                    miss_sound.play()  # Play the hiss sound
                    show_scratch = True

                display_surface.blit(scratch_image, scratch_rect)
                display_surface.blit(game_over_text, game_over_rect)
                display_surface.blit(continue_text, continue_rect)
                pygame.display.update()

                # Save high score
                save_high_score(high_score)

                # Wait for any key press to restart
                waiting_for_key = True
                while waiting_for_key:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting_for_key = False
                        if event.type == pygame.KEYDOWN:
                            # Reset game state
                            score = 0
                            player_lives = PLAYER_STARTING_LIVES
                            food_velocity = FOOD_STARTING_VELOCITY
                            player_rect = scaled_image_closed.get_rect()
                            player_rect.left = 32
                            player_rect.centery = WINDOW_HEIGHT // 2
                            reset_food()
                            show_scratch = False
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