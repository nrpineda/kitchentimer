# Example file showing a circle moving on screen
import pygame
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    #pygame.draw.circle(screen, "red", player_pos, 40)

    # pick a font you have and set its size
    myfont = pygame.font.SysFont("Helvetica", 30)
    # apply it to text on a label
    label = myfont.render("1904", 1, "pink")
    # put the label object on the screen at point x=100, y=100
    screen.blit(label, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()