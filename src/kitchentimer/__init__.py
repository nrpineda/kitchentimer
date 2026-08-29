import pygame
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720
seconds_remaining = 180

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # pick a font you have and set its size
    myfont = pygame.font.SysFont("Segoe UI", 50)
    # apply it to text on a label
    minutes = int(seconds_remaining) //60
    # s=str(s)
    s = f"{minutes:02d}:{int(seconds_remaining)}" # "02:00"
    
    label = myfont.render(s, 1, "pink")
    # put the label object on the screen at point x=100, y=100
    screen.blit(label, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    seconds_remaining = seconds_remaining - dt
    print(seconds_remaining)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()