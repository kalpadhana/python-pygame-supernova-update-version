# ████████████████████████████████████████████████████████████████████████████████
# ██                           MAIN MENU SYSTEM                                 ██
# ████████████████████████████████████████████████████████████████████████████████

# === IMPORTS AND DEPENDENCIES ===
import sys
import random

import pygame
import pygame.mixer

from classes.constants import WIDTH, HEIGHT, BLACK, WHITE, RED


# === VISUAL EFFECTS ===
def animate_screen():
    
    for i in range(0, 20):
        screen.blit(mainmenu_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        
        screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
        pygame.display.flip()
        pygame.time.wait(10)


# === PYGAME AND AUDIO INITIALIZATION ===
pygame.mixer.init()
pygame.init()

pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)

pygame.mixer.set_num_channels(20)
for i in range(20):
    channel = pygame.mixer.Channel(i)
    channel.set_volume(0.25)

# === DISPLAY AND VISUAL SETUP ===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

mainmenu_img = pygame.image.load('images/mainmenu..jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

logo_img = pygame.image.load('images/ch.png').convert_alpha()
logo_x = (WIDTH - logo_img.get_width()) // 2
logo_y = 50

# === BUTTON LAYOUT AND POSITIONING ===
play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 205, 50)

# === AUDIO AND MENU STATE SETUP ===
pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.play(-1)

explosion_sound = pygame.mixer.Sound('game_sounds/explosions/explosion1.wav')
explosion_sound.set_volume(0.25)

selected_button = 0
show_menu = True

# === JOYSTICK/GAMEPAD INITIALIZATION ===
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


# === MAIN MENU LOOP ===
while show_menu:
    # === EVENT PROCESSING ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # === MOUSE INPUT HANDLING ===
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            if play_button_rect.collidepoint(x, y):
                explosion_sound.play()
                animate_screen()
                show_menu = False
                import main
                main.main()
                break
            
            elif quit_button_rect.collidepoint(x, y):
                pygame.quit()
                sys.exit()

        # === KEYBOARD INPUT HANDLING ===
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_button = 0
            elif event.key == pygame.K_DOWN:
                selected_button = 1
            elif event.key == pygame.K_RETURN:
                if selected_button == 0:
                    explosion_sound.play()
                    animate_screen()
                    show_menu = False
                    screen.fill(BLACK)
                    import main
                    main.main()
                    break
                elif selected_button == 1:
                    pygame.quit()
                    sys.exit()

        # === JOYSTICK/GAMEPAD INPUT HANDLING ===
        if joystick:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if selected_button == 0:
                        explosion_sound.play()
                        animate_screen()
                        show_menu = False
                        screen.fill(BLACK)
                        import main
                        main.main()
                        break
                    elif selected_button == 1:
                        pygame.quit()
                        sys.exit()
            
            elif event.type == pygame.JOYHATMOTION:
                if event.value[1] == 1:
                    selected_button = 0
                elif event.value[1] == -1:
                    selected_button = 1

    # === MENU RENDERING ===
    screen.blit(mainmenu_img, (0, 0))

    screen.blit(logo_img, (logo_x, logo_y))

    # === BUTTON RENDERING ===
    font = pygame.font.SysFont('Comic Sans MS', 40)
    
    text = font.render("Play", True, WHITE)
    pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
    
    if selected_button == 0:
        pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
    
    text_rect = text.get_rect()
    text_rect.center = play_button_rect.center
    screen.blit(text, text_rect)
    
    text = font.render("Exit", True, WHITE)
    pygame.draw.rect(screen, BLACK, quit_button_rect, border_radius=10)
    
    if selected_button == 1:
        pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10, width=4)
    
    text_rect = text.get_rect()
    text_rect.center = quit_button_rect.center
    screen.blit(text, text_rect)
    
    # === DISPLAY UPDATE ===
    pygame.display.flip()
    clock.tick(60)

# === CLEANUP ===
pygame.quit()
