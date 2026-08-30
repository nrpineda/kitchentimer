import pygame
import os

# pygame setup
pygame.init()
background = pygame.image.load(os.path.join("images", "peakpx.jpg"))
screen = pygame.display.set_mode(background.get_size())
clock = pygame.time.Clock()
running = True
dt = 0
total_seconds_remaining = 10.0

is_alarm_played = False
button_was_clicked = False

button_position = (background.get_size()[0]*0.10, background.get_size()[1]*0.15)
button_image = pygame.image.load(os.path.join("images", "timer.png")) 


def process(screen: pygame.Surface, dt: float):
    global is_alarm_played

    ## BACKGROUND
    screen.blit(background)

    if button_was_clicked:
        if total_seconds_remaining <= 0:
            if not is_alarm_played:
                # play_alarm_sound()
                is_alarm_played = True
            
            if first_half_of_second(total_seconds_remaining):
                pass # hide timer
            else:
                draw_timer(screen)
        
        else:
            draw_timer(screen)

        count_down(dt)
    else:
        draw_button(screen)
        process_button()


def first_half_of_second(seconds: float):
    fraction = get_fraction(seconds)
    return fraction < 0.5


def get_fraction(x: float):
    float_as_string = str(x) # '5.051' -> .051
    whole, frac = float_as_string.split('.') # split to ['5', '051']
    return float(f"0.{frac}")


def count_down(dt):
    global total_seconds_remaining
    total_seconds_remaining = total_seconds_remaining - dt


def draw_timer(screen):
    button_center = vec_sum(button_position, button_image.get_rect().center)
    formatted_time_string = format_time(total_seconds_remaining)
    draw_text(screen, formatted_time_string, position=button_center)


def process_button():
    global button_was_clicked
    rectangle = button_image.get_rect()
    rectangle = rectangle.move(button_position)
    if button_just_clicked(rectangle):
        button_was_clicked = not button_was_clicked


def draw_button(screen: pygame.Surface):
    screen.blit(button_image, button_position)


def button_just_clicked(rect):
    return mouse_cursor_within_button(rect) and mouse_was_clicked()


def mouse_cursor_within_button(rect):
    t = rect.collidepoint(pygame.mouse.get_pos())
    return t

def mouse_was_clicked():
    return pygame.mouse.get_just_pressed()[0]


def draw_text(screen: pygame.Surface, s: str, position: pygame.typing.Point, centered=True):
    myfont = pygame.font.SysFont("Helvetica", 50)
    label = myfont.render(s, True, "pink")
    label_center = label.get_rect().center
    if centered:
        offset = vec_diff(position, label_center)
        screen.blit(label, offset)
    else:
        screen.blit(label, position)


def vec_diff(end_point: pygame.typing.Point, start_point: pygame.typing.Point) -> pygame.typing.Point:
    return (
        end_point[0] - start_point[0],
        end_point[1] - start_point[1],
    )


def vec_sum(a: pygame.typing.Point, b: pygame.typing.Point) -> pygame.typing.Point:
    return (
        a[0] + b[0],
        a[1] + b[1],
    )


def format_time(total_seconds: float):
    t = abs(total_seconds)
    minutes_and_seconds = (t) / 60
    minutes = int(minutes_and_seconds)
    seconds = (minutes_and_seconds - minutes) * 60
    negative = total_seconds < 0
    return f"{'-' if negative else ''}{minutes:02d}:{int(seconds):02d}" # "02:00"


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