import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
HERO_SIZE = 150
ENEMY_SIZE = 70
BULLET_SIZE = 40
ENEMY_SPEED = 1.5
BACKGROUND_SPEED = 1
button_font = pygame.font.Font(None, 36)

# Set up some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load the images
hero_img = pygame.image.load('hero.png')
hero_img = pygame.transform.scale(hero_img, (HERO_SIZE, HERO_SIZE))

enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))

bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (BULLET_SIZE, BULLET_SIZE))

background_img = pygame.image.load('space.jpg')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load the audio files
pygame.mixer.music.load('background_music.mp3')
death_sound = pygame.mixer.Sound('death_sound.mp3')
lose = pygame.mixer.Sound('lose_sound.mp3')
intro = pygame.mixer.Sound('intro.mp3')
wow  = pygame.mixer.Sound('wow.mp3')
shoot_sounds = [
    pygame.mixer.Sound('pew1.mp3'),
    pygame.mixer.Sound('pew2.mp3'),
    pygame.mixer.Sound('pew3.mp3'),
    # Add more bullet sound options as needed
]
# Set up the font
font = pygame.font.Font(None, 36)

# Set up the rules
rules = [
    "Use the arrow keys to move the hero",
    "Press the space bar to shoot",
    "Avoid the enemies!"
]

# Set up the start button
start_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 25, 200, 50)
#bullet selection button
bullet_sound_buttons = []
button_spacing = 100
for i in range(len(shoot_sounds)):
    button_rect = pygame.Rect(WIDTH / 2 - 150 + i * button_spacing, HEIGHT / 2 + 50, 100, 50)
    bullet_sound_buttons.append(button_rect)

# Selected bullet sound index (default to the first sound)
selected_bullet_sound = 0
# Set up the retry button
retry_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 50, 200, 50)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("earth shooter")

# Game state variables
start_game = False
game_over = False
hero_x, hero_y = WIDTH / 2, HEIGHT - HERO_SIZE - 20
enemy_x, enemy_y = random.randint(0, WIDTH - ENEMY_SIZE), 0
bullets = []
score = 0

# Initialize background position
background_img_y = 0

# Function to draw the start screen
def draw_start_screen():

    screen.blit(background_img, (0, background_img_y))
    screen.blit(background_img, (0, background_img_y - HEIGHT))
    for i, rule in enumerate(rules):
        text = font.render(rule, True, WHITE)
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 50 + i * 30))
    pygame.draw.rect(screen, WHITE, start_button)
    text = font.render("Start", True, BLACK)
    screen.blit(text, (start_button.x + 75, start_button.y + 15))
    text = font.render("Select the sound u want for gun",True,WHITE)
    screen.blit(text, (start_button.x + -50, start_button.y + 50))
     # Draw bullet sound selection buttons
    for i, button_rect in enumerate(bullet_sound_buttons):
        pygame.draw.rect(screen, WHITE, button_rect)
        text = button_font.render("Sound " + str(i + 1), True, BLACK)
        screen.blit(text, (button_rect.x + 15, button_rect.y + 15))

    # Function to handle input on the start screen
def handle_start_input():
    global selected_bullet_sound
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                pygame.mixer.music.play(-1)  # Start background music
                return True  # Return True to indicate start game
            # Check bullet sound selection
            for i, button_rect in enumerate(bullet_sound_buttons):
                if button_rect.collidepoint(event.pos):
                    selected_bullet_sound = i  # Set selected bullet sound index
                    break
    return False 


# Function to draw the game screen
def draw_game_screen():
    screen.blit(background_img, (0, background_img_y))
    screen.blit(background_img, (0, background_img_y - HEIGHT))
    screen.blit(hero_img, (hero_x, hero_y))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))  # Draw bullet image
    screen.blit(enemy_img, (enemy_x, enemy_y))
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

# Function to draw the game over screen
def draw_game_over_screen():
    screen.blit(background_img, (0, background_img_y))
    screen.blit(background_img, (0, background_img_y - HEIGHT))
    text = font.render("Game Over! Your score was " + str(score), True, WHITE)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.draw.rect(screen, WHITE, retry_button)
    text = font.render("Retry", True, BLACK)
    screen.blit(text, (retry_button.x + 75, retry_button.y + 15))

#ha gle user input 
def handle_input():
    global hero_x, bullets, start_game, game_over, selected_bullet_sound
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos) and not start_game:
                start_game = True
                game_over = False
                pygame.mixer.music.play(-1)
                intro.stop()
            if retry_button.collidepoint(event.pos) and game_over:
                reset_game()
                wow.play()
                pygame.mixer.music.play(-1)
            # Check bullet sound selection
            for i, button_rect in enumerate(bullet_sound_buttons):
                if button_rect.collidepoint(event.pos):
                    selected_bullet_sound = i  # Set selected bullet sound index
                    break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start_game:
                # Play selected bullet sound
                shoot_sounds[selected_bullet_sound].play()
                bullets.append([hero_x + HERO_SIZE / 2 - BULLET_SIZE / 2, hero_y])  # Adjust bullet position

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        hero_x -= 5
    if keys[pygame.K_RIGHT]:
        hero_x += 5


# Function to reset the game state
def reset_game():
    global hero_x, hero_y, enemy_x, enemy_y, bullets, score, game_over, start_game
    hero_x, hero_y = WIDTH / 2, HEIGHT - HERO_SIZE - 20
    enemy_x, enemy_y = random.randint(0, WIDTH - ENEMY_SIZE), 0
    bullets = []
    score = 0
    game_over = False
    start_game = True
    lose.stop()

# Function to update game logic
def update_game():
    global hero_x, hero_y, enemy_x, enemy_y, bullets, score, game_over

    hero_x = max(0, min(hero_x, WIDTH - HERO_SIZE))
    hero_y = max(0, min(hero_y, HEIGHT - HERO_SIZE))

    for i, bullet in enumerate(bullets):
        bullet[1] -= 5
        if bullet[1] < 0:
            bullets.pop(i)

    if enemy_y > HEIGHT:
        enemy_x, enemy_y = random.randint(0, WIDTH - ENEMY_SIZE), 0
    enemy_y += ENEMY_SPEED

    for i, bullet in enumerate(bullets):
        if (enemy_x < bullet[0] < enemy_x + ENEMY_SIZE and
                enemy_y < bullet[1] < enemy_y + ENEMY_SIZE):
            bullets.pop(i)
            enemy_x, enemy_y = random.randint(0, WIDTH - ENEMY_SIZE), 0
            death_sound.play()
            score += 1
            break

    if (enemy_x < hero_x + HERO_SIZE and
            enemy_x + ENEMY_SIZE > hero_x and
            enemy_y < hero_y + HERO_SIZE and
            enemy_y + ENEMY_SIZE > hero_y):
        game_over = True
        lose.play()
        pygame.mixer.music.stop()
intro.play()
# Initialize game clock
clock = pygame.time.Clock()

# Main game loop
while True:
    handle_input()
    
    if not start_game:
        draw_start_screen()
    elif game_over:
        draw_game_over_screen()
    else:
        update_game()
        draw_game_screen()

    background_img_y += BACKGROUND_SPEED
    if background_img_y >= HEIGHT:
        background_img_y = 0

    pygame.display.flip()

    clock.tick(60)
