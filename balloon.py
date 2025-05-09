import pygame
import pymunk
import pymunk.pygame_util
import random

# Init
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Balloon Pop Game")

# Load assets
balloon_image = pygame.transform.scale(pygame.image.load("balloon.png"), (150, 150))
background = pygame.transform.scale(pygame.image.load("balloonbg.jpg"), (800, 600))
pop_sound = pygame.mixer.Sound("pop.mp3")
pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Setup
space = pymunk.Space()
space.gravity = (0, -50)

score = 0
target_score = 1500  # 20 balloons * 100
balloons = []

frame_count = 0
max_frames = 900  # 30 seconds at 60 fps
game_over = False
won = False

def create_balloon():
    x = random.randint(75, 725)
    y = 500
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 25))
    body.position = x, y
    shape = pymunk.Circle(body, 25)
    shape.elasticity = 0
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape

# Main loop
running = True
while running:
    screen.blit(background, (0, 0))
    frame_count += 1

    if not game_over and random.randint(1, 30) == 1:
        balloons.append(create_balloon())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

            for body, shape in balloons[:]:
                x, y = body.position
                balloon_rect = pygame.Rect(x - 75, y - 75, 150, 150)
                if balloon_rect.colliderect(mouse_rect):
                    pop_sound.play()
                    balloons.remove((body, shape))
                    space.remove(body, shape)
                    score += 100

    # Remove balloons off screen
    for body, shape in balloons[:]:
        x, y = body.position
        screen.blit(balloon_image, (x - 75, y - 75))
        if y < -100:
            balloons.remove((body, shape))
            space.remove(body, shape)

    # Game state
    if not game_over:
        if score >= target_score:
            game_over = True
            won = True
        elif frame_count >= max_frames:
            game_over = True
            won = False

    # HUD
    font = pygame.font.SysFont(None, 36)
    time_left = max(0, (max_frames - frame_count) // 60)
    screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(f"Time Left: {time_left}s", True, (0, 0, 0)), (600, 10))

    if game_over:
        msg = "YOU WIN!" if won else "GAME OVER"
        big_font = pygame.font.SysFont(None, 72)
        text = big_font.render(msg, True, (255, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 250))

    space.step(1/60)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
