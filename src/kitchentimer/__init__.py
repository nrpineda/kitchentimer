import pygame
import os
SCREEN_WIDTH=1008
SCREEN_HEIGHT=536

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
total_seconds_remaining = 150

def process(screen: pygame.Surface, dt: float):

    global total_seconds_remaining 
    background = pygame.image.load(os.path.join("images", "background_1.png"))
    screen.blit(background)
    s = format_time(total_seconds_remaining)
    draw_text(screen, s, x = SCREEN_WIDTH/4, y = SCREEN_HEIGHT/4)
    draw_text(screen, s, x = SCREEN_WIDTH/2, y = SCREEN_HEIGHT/2)
    total_seconds_remaining = total_seconds_remaining - dt

def draw_text(screen: pygame.Surface, s: str, x: int, y: int):
    myfont = pygame.font.SysFont("Helvetica", 50)
    label = myfont.render(s, 1, "pink")
    screen.blit(label, (x, y))

def format_time(total_seconds:float):
    minutes_and_seconds = (total_seconds) / 60
    minutes = int(minutes_and_seconds)
    seconds = (minutes_and_seconds - minutes) *60
    return f"{minutes:02d}:{int(seconds):02d}" # "02:00"

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    process(screen, dt)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()