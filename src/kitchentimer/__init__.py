import pygame
import os
from enum import StrEnum

EGG_COOK_TIME_SECONDS = 10.0

# pygame setup
pygame.init()
background = pygame.image.load(os.path.join("images", "peakpx.jpg"))
screen = pygame.display.set_mode(background.get_size())
clock = pygame.time.Clock()
running = True
dt = 0
total_seconds_remaining = EGG_COOK_TIME_SECONDS

class TimerState(StrEnum):
    STOPPED = 'Stopped'
    RUNNING = 'Running'
    OVERTIME = 'Overtime'
    PAUSED = 'Paused'
    FINAL_HOLD = 'Final Hold'

timer_state: TimerState = TimerState.STOPPED

button_position = (background.get_size()[0]*0.10, background.get_size()[1]*0.15)
button_image = pygame.image.load(os.path.join("images", "timer2.png")) 
alarm_sound = pygame.mixer.Sound("audio/freesound_community-alarm-clock-short-6402.mp3")
sizzling_sound = pygame.mixer.Sound("audio/oxidvideos-sizzlingcooking-eggs-414333.mp3")

## 'process' functions will be called every frame, and have some code that executes (most likely)
## 'handle' functions may still be called every frame, but are typically checking for a condition so as to execute only once before changing states.
def process(screen: pygame.Surface, dt: float):
    ## BACKGROUND
    screen.blit(background)
    draw_text(screen=screen, s=timer_state, position=(400, 100)) ## debug state display

    if timer_state == TimerState.STOPPED:
        process_state_stopped(screen)
    elif timer_state == TimerState.RUNNING:
        process_state_running(screen, dt)
    elif timer_state == TimerState.OVERTIME:
        process_state_overtime(screen, dt)
    elif timer_state == TimerState.PAUSED:
        process_state_paused(screen)
    elif timer_state == TimerState.FINAL_HOLD:
        process_state_final_hold(screen)
    else:
        print('WARNING: Invalid timer state.')


def process_state_paused(screen):
    draw_timer(screen)
    handle_transition_run()


def process_state_final_hold(screen):
    draw_timer(screen)
    handle_transition_reset()


def process_state_running(screen, dt):
    draw_timer(screen)
    count_down(dt)
    
    if total_seconds_remaining <= 0:
        set_timer_state(TimerState.OVERTIME)
        alarm_sound.play(loops=-1)
    
    handle_transition_pause()


def process_state_overtime(screen, dt):
    if first_half_of_second(total_seconds_remaining):
        pass # hide timer
    else:
        draw_timer(screen)

    count_down(dt)
    handle_transition_hold()


def process_state_stopped(screen):
    draw_button(screen)
    handle_transition_run()


def first_half_of_second(seconds: float):
    fraction = get_fraction(seconds)
    return fraction < 0.5


def get_fraction(x: float):
    float_as_string = str(x) # '5.051' -> .051
    whole, frac = float_as_string.split('.') # split to ['5', '051']
    return float(f"0.{frac}")


def count_down(dt):
    set_total_seconds_remaining(total_seconds_remaining - dt)


def draw_timer(screen):
    button_center = vec_sum(button_position, button_image.get_rect().center)
    formatted_time_string = format_time(total_seconds_remaining)
    draw_text(screen, formatted_time_string, position=button_center)


## Maybe some of these handlers will listen for RMB or for a continuous click,
## or for a key + click.
## So I think it's acceptable to leave the duplicate "if button_just_clicked():" for now.
def handle_transition_run():
    if button_just_clicked():
        set_timer_state(TimerState.RUNNING)


def handle_transition_pause():
    if button_just_clicked():
        set_timer_state(TimerState.PAUSED)


def handle_transition_hold():
    if button_just_clicked():
        set_timer_state(TimerState.FINAL_HOLD)
        alarm_sound.stop()


def handle_transition_reset():
    if button_just_clicked():
        set_timer_state(TimerState.STOPPED)
        set_total_seconds_remaining(EGG_COOK_TIME_SECONDS)


def button_just_clicked() -> bool:
    button_rect = button_image.get_rect()
    button_rect = button_rect.move(button_position)
    return rect_just_clicked(button_rect)


def set_timer_state(x: TimerState):
    global timer_state
    timer_state = x


def set_total_seconds_remaining(x: float):
    global total_seconds_remaining
    total_seconds_remaining = x


def draw_button(screen: pygame.Surface):
    screen.blit(button_image, button_position)


def rect_just_clicked(rect):
    return mouse_cursor_within_rect(rect) and mouse_was_clicked()


def mouse_cursor_within_rect(rect):
    t = rect.collidepoint(pygame.mouse.get_pos())
    return t


def mouse_was_clicked():
    return pygame.mouse.get_just_pressed()[0]


def draw_text(screen: pygame.Surface, s: str, position: pygame.typing.Point, centered=True):
    myfont = pygame.font.SysFont("Cooper Black", 50)
    label = myfont.render(s, True, "black")
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