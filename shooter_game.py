import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 1280, 720

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
HOVER_COLOR = (50, 150, 50)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shooter Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 250

# Load assets
menu_background = pygame.image.load("background.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

background = pygame.image.load("background (2).png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

bow_image = pygame.image.load("bow.png")
bow_width, bow_height = 170, 100
bow_image = pygame.transform.scale(bow_image, (bow_width, bow_height))

arrow_image = pygame.image.load("arrow.jpg")
arrow_width, arrow_height = 10, 50
arrow_image = pygame.transform.scale(arrow_image, (arrow_width, arrow_height))

enemy_image = pygame.image.load("enemy1.png")
enemy_width, enemy_height = 100, 100
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

human_image = pygame.image.load("sheep.png")
human_width, human_height = 100, 100
human_image = pygame.transform.scale(human_image, (human_width, human_height))

pause_icon = pygame.image.load("pause.png")
pause_icon = pygame.transform.scale(pause_icon, (50, 50))

# Load sound effects
shoot_sound = pygame.mixer.Sound("shoot_sound.wav")
hit_sound = pygame.mixer.Sound("hit_sound.wav")
human_hit_sound = pygame.mixer.Sound("hit_sound.wav")

# Font settings
title_font = pygame.font.SysFont("Arial", 72, bold=True)
button_font = pygame.font.SysFont("Arial", 36, bold=True)
game_over_font = pygame.font.SysFont("Arial", 48, bold=True)

# Player settings
player_x, player_y = WIDTH // 2, HEIGHT - 100
player_speed = 8

# Bullet settings
bullets = []
bullet_speed = -7
bullet_cooldown = 500
last_shot_time = 0

# Enemy and human settings
enemies = []
humans = []
enemy_speed = 1
human_speed = 1
enemy_spawn_chance = 0.02
human_spawn_chance = 0.01
max_enemies = 5
max_humans = 1

# Score and lives
score = 0
lives = 10

# Difficulty settings
difficulty_thresholds = [500, 1000, 2000, 4000]
difficulty_levels = [
    {"enemy_speed": 2, "max_enemies": 7, "enemy_spawn_chance": 0.03},
    {"enemy_speed": 3, "max_enemies": 10, "enemy_spawn_chance": 0.04},
    {"enemy_speed": 4, "max_enemies": 12, "enemy_spawn_chance": 0.05},
    {"enemy_speed": 5, "max_enemies": 15, "enemy_spawn_chance": 0.06},
]
current_difficulty_level = 0

# Load background music and start playing
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)

# Function to draw text
def draw_text(text, font, color, x, y, center=True):
    label = font.render(text, True, color)
    if center:
        x -= label.get_width() // 2
        y -= label.get_height() // 2
    screen.blit(label, (x, y))

# Function to reset the game
def reset_game():
    global player_x, bullets, enemies, humans, score, lives, enemy_speed, current_difficulty_level
    player_x = WIDTH // 2
    bullets.clear()
    enemies.clear()
    humans.clear()
    score = 0
    lives = 3
    enemy_speed = 1
    current_difficulty_level = 0

# Function to spawn enemies
def spawn_enemy():
    if len(enemies) < max_enemies:
        while True:
            enemy_x = random.randint(50, WIDTH - enemy_width)
            enemy_y = -enemy_height
            new_enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
            if not any(new_enemy.colliderect(enemy) for enemy in enemies):
                enemies.append(new_enemy)
                break

# Function to spawn humans
def spawn_human():
    if len(humans) < max_humans:
        while True:
            human_x = random.randint(50, WIDTH - human_width)
            human_y = -human_height
            new_human = pygame.Rect(human_x, human_y, human_width, human_height)
            if not any(new_human.colliderect(human) for human in humans):
                humans.append(new_human)
                break

# Function to display the main menu
def main_menu():
    menu_running = True
    play_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 100)

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    menu_running = False

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(menu_background, (0, 0))
        draw_text("2D Shooter Game", title_font, WHITE, WIDTH // 2, HEIGHT // 3)
        button_color = HOVER_COLOR if play_button.collidepoint(mouse_pos) else GREEN
        pygame.draw.rect(screen, button_color, play_button, border_radius=10)
        draw_text("PLAY", button_font, BLACK, play_button.centerx, play_button.centery)

        pygame.display.flip()
        clock.tick(FPS)

# Function to draw the pause icon
def draw_pause_icon():
    pause_rect = pygame.Rect(WIDTH - 60, 10, 50, 50)
    screen.blit(pause_icon, pause_rect)

# Function to update difficulty
def update_difficulty():
    global enemy_speed, max_enemies, enemy_spawn_chance, current_difficulty_level
    if current_difficulty_level < len(difficulty_thresholds):
        if score >= difficulty_thresholds[current_difficulty_level]:
            settings = difficulty_levels[current_difficulty_level]
            enemy_speed = settings["enemy_speed"]
            max_enemies = settings["max_enemies"]
            enemy_spawn_chance = settings["enemy_spawn_chance"]
            current_difficulty_level += 1

# Run the main menu
main_menu()

# Main game loop
running = True
paused = False
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pause_rect = pygame.Rect(WIDTH - 60, 10, 50, 50)
            if pause_rect.collidepoint(event.pos):
                paused = not paused

    if not paused and not game_over:
        update_difficulty()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - bow_width:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time > bullet_cooldown:
                bullet_rect = pygame.Rect(player_x + bow_width // 2 - arrow_width // 2, player_y, arrow_width, arrow_height)
                bullets.append(bullet_rect)
                shoot_sound.play()
                last_shot_time = current_time

        if random.random() < enemy_spawn_chance:
            spawn_enemy()

        if random.random() < human_spawn_chance:
            spawn_human()

        for bullet in bullets[:]:
            bullet.y += bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                lives -= 1
                if lives <= 0:
                    game_over = True
            for bullet in bullets[:]:
                if enemy.colliderect(bullet):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 100
                    hit_sound.play()

        for human in humans[:]:
            human.y += human_speed
            if human.y > HEIGHT:
                humans.remove(human)

            for bullet in bullets[:]:
                if human.colliderect(bullet):
                    humans.remove(human)
                    bullets.remove(bullet)
                    lives -= 1
                    human_hit_sound.play()
                    if lives <= 0:
                        game_over = True

    screen.blit(background, (0, 0))
    if game_over:
        draw_text("GAME OVER", game_over_font, (255, 0, 0), WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press R to Restart", button_font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
            game_over = False
    else:
        screen.blit(bow_image, (player_x, player_y))
        for bullet in bullets:
            screen.blit(arrow_image, bullet)
        for enemy in enemies:
            screen.blit(enemy_image, enemy)
        for human in humans:
            screen.blit(human_image, human)
        draw_text(f"Score: {score}", button_font, WHITE, 100, 50, center=False)
        draw_text(f"Lives: {lives}", button_font, WHITE, WIDTH - 150, 50, center=False)
        draw_pause_icon()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
