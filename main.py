# ████████████████████████████████████████████████████████████████████████████████
# ██                          SETUP AND INITIALIZATION                          ██
# ████████████████████████████████████████████████████████████████████████████████

# === IMPORTS AND DEPENDENCIES ===
import sys

import pygame
import random

from controls import move_player, move_player_with_joystick
from classes.constants import WIDTH, HEIGHT, FPS, SHOOT_DELAY
from functions import show_game_over, music_background

# === MODERN UI IMPORTS ===
from modern_ui import ModernHealthBar, ModernScore
from particle_effects import ParticleSystem
from leaderboard import Leaderboard

# === ADVANCED SYSTEMS IMPORTS ===
from achievements import AchievementSystem
from game_difficulty import GameDifficulty
from powerups import PowerUpManager
from weapons import WeaponSystem, AbilitySystem
from game_modes import GameModeManager, GameState
from enemy_types import AdvancedEnemyTypeManager, get_behavior_function
from sound_manager import SoundManager, SoundEventBus
from visual_effects import EffectsManager
from advanced_menus import PauseMenu, SettingsMenu, GameModeSelectorMenu
from modern_features import DamageNumberManager, DroneManager, DashSystem, UltimateSystem, LevelSystem

from classes.player import Player
from classes.bullets import Bullet
from classes.refill import BulletRefill, HealthRefill, DoubleRefill, ExtraScore
from classes.meteors import Meteors, Meteors2, BlackHole
from classes.explosions import Explosion, Explosion2
from classes.enemies import Enemy1, Enemy2
from classes.bosses import Boss1, Boss2, Boss3


# === PYGAME INITIALIZATION ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Super Nova - Modern Edition")
clock = pygame.time.Clock()

# === MODERN UI INITIALIZATION ===
health_bar = ModernHealthBar(10, 10, width=200, height=30, max_hp=200)
score_display = ModernScore(WIDTH - 250, 10)
particles = ParticleSystem()
leaderboard = Leaderboard()

# === ADVANCED SYSTEMS INITIALIZATION ===
achievement_system = AchievementSystem()
difficulty_system = GameDifficulty()
game_state = GameState()
powerup_manager = PowerUpManager()
weapon_system = WeaponSystem()
ability_system = AbilitySystem()
game_mode_manager = GameModeManager()
enemy_type_manager = AdvancedEnemyTypeManager()
sound_manager = SoundManager()
sound_event_bus = SoundEventBus(sound_manager)
effects_manager = EffectsManager((WIDTH, HEIGHT))
pause_menu = PauseMenu(WIDTH, HEIGHT)
settings_menu = SettingsMenu(WIDTH, HEIGHT)

damage_numbers = DamageNumberManager()
drone_manager = DroneManager()
dash_system = DashSystem()
ultimate_system = UltimateSystem()
level_system = LevelSystem()
level_up_selected_idx = 0


# === SPRITE GROUPS INITIALIZATION ===
explosions = pygame.sprite.Group()
explosions2 = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy1_group = pygame.sprite.Group()
enemy2_group = pygame.sprite.Group()
boss1_group = pygame.sprite.Group()
boss2_group = pygame.sprite.Group()
boss3_group = pygame.sprite.Group()
bullet_refill_group = pygame.sprite.Group()
health_refill_group = pygame.sprite.Group()
double_refill_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
meteor2_group = pygame.sprite.Group()
extra_score_group = pygame.sprite.Group()
black_hole_group = pygame.sprite.Group()
enemy2_bullets = pygame.sprite.Group()

boss1_bullets = pygame.sprite.Group()
boss2_bullets = pygame.sprite.Group()
boss3_bullets = pygame.sprite.Group()

# === BOSS HEALTH AND STATUS TRACKING ===
boss1_health = 150
boss1_health_bar_rect = pygame.Rect(0, 0, 150, 5)
boss1_spawned = False

boss2_health = 150
boss2_health_bar_rect = pygame.Rect(0, 0, 150, 5)
boss2_spawned = False

boss3_health = 200
boss3_health_bar_rect = pygame.Rect(0, 0, 200, 5)
boss3_spawned = False

# === BACKGROUND SCROLLING SYSTEM ===
bg_y_shift = -HEIGHT
background_img = pygame.image.load('images/bg/background.jpg').convert()
background_img2 = pygame.image.load('images/bg/background2.png').convert()
background_img3 = pygame.image.load('images/bg/background3.png').convert()
background_img4 = pygame.image.load('images/bg/background4.png').convert()
background_top = background_img.copy()
current_image = background_img
new_background_activated = False

# ████████████████████████████████████████████████████████████████████████████████
# ██                             ASSET LOADING                                  ██
# ████████████████████████████████████████████████████████████████████████████████

# === VISUAL EFFECTS AND ANIMATION ASSETS ===
explosion_images = [pygame.image.load(f"images/explosion/explosion{i}.png") for i in range(8)]
explosion2_images = [pygame.image.load(f"images/explosion2/explosion{i}.png") for i in range(18)]
explosion3_images = [pygame.image.load(f"images/explosion3/explosion{i}.png") for i in range(18)]

# === ENEMY AND BOSS SPRITE ASSETS ===
enemy1_img = [
    pygame.image.load('images/enemy/enemy1_1.png').convert_alpha(),
    pygame.image.load('images/enemy/enemy1_2.png').convert_alpha(),
    pygame.image.load('images/enemy/enemy1_3.png').convert_alpha()
]
enemy2_img = [
    pygame.image.load('images/enemy/enemy2_1.png').convert_alpha(),
    pygame.image.load('images/enemy/enemy2_2.png').convert_alpha()
]
boss1_img = pygame.image.load('images/boss/boss1.png').convert_alpha()
boss2_img = pygame.image.load('images/boss/boss2_1.png').convert_alpha()
boss3_img = pygame.image.load('images/boss/boss3.png').convert_alpha()

# === POWER-UP AND COLLECTIBLE ASSETS ===
health_refill_img = pygame.image.load('images/refill/health_refill.png').convert_alpha()
bullet_refill_img = pygame.image.load('images/refill/bullet_refill.png').convert_alpha()
double_refill_img = pygame.image.load('images/refill/double_refill.png').convert_alpha()

# === OBSTACLE AND HAZARD ASSETS ===
meteor_imgs = [
    pygame.image.load('images/meteors/meteor_1.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor_2.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor_3.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor_4.png').convert_alpha()
]
meteor2_imgs = [
    pygame.image.load('images/meteors/meteor2_1.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor2_2.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor2_3.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor2_4.png').convert_alpha()
]
extra_score_img = pygame.image.load('images/score/score_coin.png').convert_alpha()
black_hole_imgs = [
    pygame.image.load('images/hole/black_hole.png').convert_alpha(),
    pygame.image.load('images/hole/black_hole2.png').convert_alpha()
]

# ████████████████████████████████████████████████████████████████████████████████
# ██                         GAME STATE MANAGEMENT                              ██
# ████████████████████████████████████████████████████████████████████████████████

# === GAME STATE VARIABLES ===
initial_player_pos = (WIDTH // 2, HEIGHT - 100)

score = 0
hi_score = 0

player = Player()
player_life = difficulty_system.get_current().player_health
player.shield = 0
player.speed_boost = 0
player.ammo = weapon_system.ammo
player.max_hp = difficulty_system.get_current().player_health
bullet_counter = weapon_system.ammo

paused = False
running = True

# === INPUT DEVICE INITIALIZATION ===
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# === MENU AND SHOOTING CONTROL SETUP ===
import menu
# Restore background music for game after menu exits
music_background()

is_shooting = False
last_shot_time = 0


# ████████████████████████████████████████████████████████████████████████████████
# ██                           MAIN GAME LOOP                                   ██
# ████████████████████████████████████████████████████████████████████████████████

# === MAIN GAME LOOP ===
while running:

    # === COLLECT EVENTS FIRST ===
    events = pygame.event.get()
    
    # === LEVEL UP MENU HANDLING ===
    if level_system.show_level_up:
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i in range(len(level_system.available_perks)):
                    rect = pygame.Rect(WIDTH//2 - 200, 200 + i * 100, 400, 80)
                    if rect.collidepoint(mouse_pos):
                        level_up_selected_idx = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    for i in range(len(level_system.available_perks)):
                        rect = pygame.Rect(WIDTH//2 - 200, 200 + i * 100, 400, 80)
                        if rect.collidepoint(mouse_pos):
                            level_up_selected_idx = i
                            perk = level_system.available_perks[level_up_selected_idx]
                            if perk["type"] == "drone":
                                drone_manager.add_drone()
                            elif perk["type"] == "health":
                                player.max_hp += 50
                                player_life = player.max_hp
                            elif perk["type"] == "firerate":
                                SHOOT_DELAY = max(50, SHOOT_DELAY - 20)
                            elif perk["type"] == "speed":
                                player.speed += 2
                            level_system.show_level_up = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    level_up_selected_idx = (level_up_selected_idx - 1) % len(level_system.available_perks)
                elif event.key == pygame.K_DOWN:
                    level_up_selected_idx = (level_up_selected_idx + 1) % len(level_system.available_perks)
                elif event.key == pygame.K_RETURN:
                    perk = level_system.available_perks[level_up_selected_idx]
                    if perk["type"] == "drone":
                        drone_manager.add_drone()
                    elif perk["type"] == "health":
                        player.max_hp += 50
                        player_life = player.max_hp
                    elif perk["type"] == "firerate":
                        SHOOT_DELAY = max(50, SHOOT_DELAY - 20)
                    elif perk["type"] == "speed":
                        player.speed += 2
                    level_system.show_level_up = False
            elif event.type == pygame.JOYHATMOTION:
                if event.value[1] == 1:
                    level_up_selected_idx = (level_up_selected_idx - 1) % len(level_system.available_perks)
                elif event.value[1] == -1:
                    level_up_selected_idx = (level_up_selected_idx + 1) % len(level_system.available_perks)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    perk = level_system.available_perks[level_up_selected_idx]
                    if perk["type"] == "drone":
                        drone_manager.add_drone()
                    elif perk["type"] == "health":
                        player.max_hp += 50
                        player_life = player.max_hp
                    elif perk["type"] == "firerate":
                        SHOOT_DELAY = max(50, SHOOT_DELAY - 20)
                    elif perk["type"] == "speed":
                        player.speed += 2
                    level_system.show_level_up = False
        
        level_system.draw_menu(screen, WIDTH, HEIGHT, level_up_selected_idx)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # === PAUSE MENU HANDLING ===
    if pause_menu.active:
        for event in events:
            pause_menu.handle_event(event)
            if event.type == pygame.QUIT:
                running = False
        
        if pause_menu.result == "resume":
            pause_menu.active = False
        elif pause_menu.result == "quit":
            running = False
        elif pause_menu.result == "menu":
            pause_menu.active = False
        
        paused = pause_menu.active
        pause_menu.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # === EVENT HANDLING ===
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not paused:
                if bullet_counter > 0 and pygame.time.get_ticks() - last_shot_time > SHOOT_DELAY:
                    last_shot_time = pygame.time.get_ticks()
                    # Use weapon system for advanced firing
                    bullets_fired = weapon_system.fire((player.rect.centerx, player.rect.top), -90, pygame.time.get_ticks())
                    for bullet_data in bullets_fired:
                        bullet = Bullet(int(bullet_data["pos"][0]), int(bullet_data["pos"][1]))
                        bullet.velocity_y = -bullet_data["speed"]
                        bullets.add(bullet)
                    bullet_counter = weapon_system.ammo
                is_shooting = True

            elif event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                dash_system.try_dash()
            elif event.key == pygame.K_RETURN and ultimate_system.charge >= ultimate_system.max_charge:
                ultimate_system.try_activate()
            elif event.key == pygame.K_p or event.key == pygame.K_PAUSE:
                pause_menu.toggle()
            elif not paused:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_UP:
                    player.move_up()
                elif event.key == pygame.K_DOWN:
                    player.move_down()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and player.original_image is not None:
                player.image = player.original_image.copy()
                is_shooting = False
            elif not paused:
                if event.key == pygame.K_LEFT:
                    player.stop_left()
                elif event.key == pygame.K_RIGHT:
                    player.stop_right()
                elif event.key == pygame.K_UP:
                    player.stop_up()
                elif event.key == pygame.K_DOWN:
                    player.stop_down()

        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0 and not paused:
                is_shooting = True
                if bullet_counter > 0 and pygame.time.get_ticks() - last_shot_time > SHOOT_DELAY:
                    last_shot_time = pygame.time.get_ticks()
                    bullets_fired = weapon_system.fire((player.rect.centerx, player.rect.top), -90, pygame.time.get_ticks())
                    for bullet_data in bullets_fired:
                        bullet = Bullet(int(bullet_data["pos"][0]), int(bullet_data["pos"][1]))
                        bullet.velocity_y = -bullet_data["speed"]
                        bullets.add(bullet)
                    bullet_counter = weapon_system.ammo
            elif event.button == 7:
                paused = not paused
            elif event.button == 3: # Y button usually
                if ultimate_system.charge >= ultimate_system.max_charge:
                    ultimate_system.try_activate()
            elif event.button == 4 or event.button == 5: # Bumpers
                dash_system.try_dash()
        elif event.type == pygame.JOYBUTTONUP:
            if event.button == 0 and player.original_image is not None:
                is_shooting = False

    # === CONTINUOUS INPUT PROCESSING ===
    if pygame.time.get_ticks() - last_shot_time > SHOOT_DELAY and is_shooting and not paused:
        if bullet_counter > 0:
            last_shot_time = pygame.time.get_ticks()
            bullets_fired = weapon_system.fire((player.rect.centerx, player.rect.top), -90, pygame.time.get_ticks())
            for bullet_data in bullets_fired:
                bullet = Bullet(int(bullet_data["pos"][0]), int(bullet_data["pos"][1]))
                bullet.velocity_y = -bullet_data["speed"]
                bullets.add(bullet)
            bullet_counter = weapon_system.ammo

    if joystick:
        if not paused:
            move_player_with_joystick(joystick, player)  

    # === PLAYER MOVEMENT AND BACKGROUND RENDERING ===
    keys = pygame.key.get_pressed()

    time_scale = ultimate_system.update()
    dash_system.update(player)
    drone_manager.update(player.rect, bullets, Bullet)

    if not paused:
        if dash_system.is_dashing:
            # maintain dashing in current direction based on last input
            pass
        else:
            move_player(keys, player)

        screen.blit(current_image, (0, bg_y_shift))
        background_top_rect = background_top.get_rect(topleft=(0, bg_y_shift))
        background_top_rect.top = bg_y_shift + HEIGHT
        screen.blit(background_top, background_top_rect)

    bg_y_shift += 1
    if bg_y_shift >= 0:
        bg_y_shift = -HEIGHT

    if score > 3000:
        bg_y_shift += 2

    # === DYNAMIC BACKGROUND SYSTEM ===
    if score >= 3000 and not new_background_activated:
        current_image = background_img2
        background_top = background_img2.copy()
        new_background_activated = True

    if score >= 10000 and new_background_activated:
        current_image = background_img3
        background_top = background_img3.copy()

    if score >= 15000 and new_background_activated:
        current_image = background_img4
        background_top = background_img4.copy()

    if score == 0:
        current_image = background_img
        background_top = background_img.copy()
        new_background_activated = False

    screen.blit(current_image, (0, bg_y_shift))
    background_top_rect = background_top.get_rect(topleft=(0, bg_y_shift))
    background_top_rect.top = bg_y_shift + HEIGHT
    screen.blit(background_top, background_top_rect)

    if score > hi_score:
        hi_score = score

# ████████████████████████████████████████████████████████████████████████████████
# ██                           ENTITY SYSTEMS                                   ██
# ████████████████████████████████████████████████████████████████████████████████

# === ENTITY SPAWNING SYSTEM ===
    if random.randint(0, 120) == 0:
        enemy_img = random.choice(enemy1_img)
        enemy_object = Enemy1(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50),
            enemy_img,
        )
        enemy1_group.add(enemy_object)

    if score >= 3000 and random.randint(0, 40) == 0 and len(enemy2_group) < 2:
        enemy_img = random.choice(enemy2_img)
        enemy2_object = Enemy2(
            random.randint(200, WIDTH - 100),
            random.randint(-HEIGHT, -100),
            enemy_img,
        )
        enemy2_group.add(enemy2_object)

    if score >= 5000 and not boss1_spawned:
        pygame.mixer.Sound('game_sounds/warning.mp3').play()
        boss1_img = boss1_img
        boss1_object = Boss1(
            random.randint(200, WIDTH - 100),
            random.randint(-HEIGHT, -100),
            boss1_img,
        )
        boss1_group.add(boss1_object)
        boss1_spawned = True

    if score >= 10000 and not boss2_spawned:
        pygame.mixer.Sound('game_sounds/warning.mp3').play()
        boss2_img = boss2_img
        boss2_object = Boss2(
            random.randint(200, WIDTH - 100),
            random.randint(-HEIGHT, -100),
            boss2_img,
        )
        boss2_group.add(boss2_object)
        boss2_spawned = True

    if score >= 15000 and not boss3_spawned:
        pygame.mixer.Sound('game_sounds/warning.mp3').play()
        boss3_img = boss3_img
        boss3_object = Boss3(
            random.randint(200, WIDTH - 100),
            random.randint(-HEIGHT, -100),
            boss3_img,
        )
        boss3_group.add(boss3_object)
        boss3_spawned = True

    if random.randint(0, 60) == 0:
        extra_score = ExtraScore(
            random.randint(50, WIDTH - 50),
            random.randint(-HEIGHT, -50 - extra_score_img.get_rect().height),
            extra_score_img,
        )
        extra_score_group.add(extra_score)

    if score > 3000 and random.randint(0, 100) == 0:
        meteor_img = random.choice(meteor_imgs)
        meteor_object = Meteors(
            random.randint(0, 50),
            random.randint(0, 50),
            meteor_img,
        )
        meteor_group.add(meteor_object)

    if random.randint(0, 90) == 0:
        meteor2_img = random.choice(meteor2_imgs)
        meteor2_object = Meteors2(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50 - meteor2_img.get_rect().height),
            meteor2_img,
        )
        meteor2_group.add(meteor2_object)

    if score > 1000 and random.randint(0, 500) == 0:
        black_hole_img = random.choice(black_hole_imgs)
        black_hole_object = BlackHole(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50 - black_hole_img.get_rect().height),
            black_hole_img,
        )
        black_hole_group.add(black_hole_object)

    # === GAME OVER AND RESET LOGIC ===
    if player_life <= 0:
        # Update achievements and stats
        achievement_system.update_progress("enemies", game_state.enemies_defeated)
        achievement_system.update_progress("bosses", game_state.bosses_defeated)
        achievement_system.update_progress("score", score)
        achievement_system.save()
        
        # Save score to leaderboard
        leaderboard.add_score(score, "Player")
        
        show_game_over(score)
        
        # Reset all systems
        boss1_spawned = False
        boss1_health = 150
        boss2_spawned = False
        boss2_health = 150
        boss3_spawned = False
        boss3_health = 200
        score = 0
        game_state.reset()
        player_life = difficulty_system.get_current().player_health
        player.max_hp = difficulty_system.get_current().player_health
        weapon_system.ammo = weapon_system.max_ammo
        bullet_counter = weapon_system.ammo
        player.rect.topleft = initial_player_pos
        bullets.empty()
        bullet_refill_group.empty()
        health_refill_group.empty()
        double_refill_group.empty()
        extra_score_group.empty()
        black_hole_group.empty()
        meteor_group.empty()
        meteor2_group.empty()
        enemy1_group.empty()
        enemy2_group.empty()
        boss1_group.empty()
        boss2_group.empty()
        boss3_group.empty()
        explosions.empty()
        explosions2.empty()
        particles.particles.clear()

# ████████████████████████████████████████████████████████████████████████████████
# ██                           COMBAT SYSTEMS                                   ██
# ████████████████████████████████████████████████████████████████████████████████

# === COLLISION DETECTION AND ENTITY UPDATES ===
    for black_hole_object in black_hole_group:
        black_hole_object.update()
        black_hole_object.draw(screen)

        if black_hole_object.rect.colliderect(player.rect):
            player_life -= 1
            black_hole_object.sound_effect.play()

        if score >= 5000:
            meteor_object.speed = 4
        if score >= 10000:
            meteor_object.speed = 4
        if score >= 15000:
            meteor_object.speed = 6
        if score >= 20000:
            meteor_object.speed = 8

    # === BULLET REFILL POWER-UP SYSTEM ===
    for bullet_refill in bullet_refill_group:
        bullet_refill.update()
        screen.blit(bullet_refill.image, bullet_refill.rect)

        if player.rect.colliderect(bullet_refill.rect):
            if weapon_system.ammo < weapon_system.max_ammo:
                weapon_system.add_ammo(50)
                bullet_counter = weapon_system.ammo
                bullet_refill.kill()
                bullet_refill.sound_effect.play()
                achievement_system.update_progress("powerups", 1)
                sound_event_bus.trigger_event("power_up_collected")
            else:
                bullet_refill.kill()
                bullet_refill.sound_effect.play()

    # === POWER-UP MANAGER UPDATE ===
    powerup_manager.update(HEIGHT)
    powerup_manager.draw(screen)
    collected = powerup_manager.check_collision(player)
    
    for powerup in collected:
        achievement_system.update_progress("powerups", 1)
        sound_event_bus.trigger_event("power_up_collected")

    # === HEALTH REFILL POWER-UP SYSTEM ===
    for health_refill in health_refill_group:
        health_refill.update()
        screen.blit(health_refill.image, health_refill.rect)

        if player.rect.colliderect(health_refill.rect):
            if player_life < player.max_hp:
                player_life += 50
                if player_life > player.max_hp:
                    player_life = player.max_hp
                health_refill.kill()
                health_refill.sound_effect.play()
                achievement_system.update_progress("powerups", 1)
                sound_event_bus.trigger_event("power_up_collected")
            else:
                health_refill.kill()
                health_refill.sound_effect.play()

    # === EXTRA SCORE COLLECTIBLE SYSTEM ===
    for extra_score in extra_score_group:
        extra_score.update()
        screen.blit(extra_score.image, extra_score.rect)

        if player.rect.colliderect(extra_score.rect):
            score += 20
            extra_score.kill()
            extra_score.sound_effect.play()

        if score >= 3000:
            extra_score.speed = 2
        if score >= 10000:
            extra_score.speed = 4
        if score >= 15000:
            extra_score.speed = 6
        if score >= 20000:
            extra_score.speed = 8

    # === DOUBLE REFILL POWER-UP SYSTEM ===
    for double_refill in double_refill_group:
        double_refill.update()
        screen.blit(double_refill.image, double_refill.rect)

        if player.rect.colliderect(double_refill.rect):
            if player_life < 200:
                player_life += 50
                if player_life > 200:
                    player_life = 200
            if bullet_counter < 200:
                bullet_counter += 50
                if bullet_counter > 200:
                    bullet_counter = 200
                double_refill.kill()
                double_refill.sound_effect.play()
            else:
                double_refill.kill()
                double_refill.sound_effect.play()

    # === METEOR COMBAT SYSTEM ===
    for meteor_object in meteor_group:
        if time_scale < 1.0:
            meteor_object.speed *= time_scale
            
        meteor_object.update()
        meteor_object.draw(screen)
        
        if time_scale < 1.0:
            meteor_object.speed /= time_scale

        if meteor_object.rect.colliderect(player.rect) and not dash_system.is_dashing:
            player_life -= 10
            damage_numbers.add(player.rect.centerx, player.rect.top, 10)
            explosion = Explosion(meteor_object.rect.center, explosion_images)
            explosions.add(explosion)
            meteor_object.kill()
            score += 50
            
        bullet_collisions = pygame.sprite.spritecollide(meteor_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion = Explosion(meteor_object.rect.center, explosion_images)
            explosions.add(explosion)
            meteor_object.kill()
            score += 80
            level_system.add_xp(20)
            ultimate_system.add_charge(15)
            game_state.enemies_defeated += 1
            achievement_system.update_progress("enemies", 1)
            sound_event_bus.trigger_event("enemy_death")
            difficulty_system.increase_progression()

            if random.randint(0, 10) == 0:
                double_refill = DoubleRefill(
                    meteor_object.rect.centerx,
                    meteor_object.rect.centery,
                    double_refill_img,
                )
                double_refill_group.add(double_refill)

        if score >= 3000:
            meteor_object.speed = 4
        if score >= 10000:
            meteor_object.speed = 6
        if score >= 15000:
            meteor_object.speed = 8
        if score >= 20000:
            meteor_object.speed = 10

    # === METEOR2 COMBAT SYSTEM ===
    for meteor2_object in meteor2_group:
        if time_scale < 1.0:
            meteor2_object.speed *= time_scale
            
        meteor2_object.update()
        meteor2_object.draw(screen)
        
        if time_scale < 1.0:
            meteor2_object.speed /= time_scale

        if meteor2_object.rect.colliderect(player.rect) and not dash_system.is_dashing:
            player_life -= 10
            damage_numbers.add(player.rect.centerx, player.rect.top, 10)
            explosion = Explosion(meteor2_object.rect.center, explosion_images)
            explosions.add(explosion)
            meteor2_object.kill()
            score += 20

        bullet_collisions = pygame.sprite.spritecollide(meteor2_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion = Explosion(meteor2_object.rect.center, explosion_images)
            explosions.add(explosion)
            meteor2_object.kill()
            score += 40
            level_system.add_xp(15)
            ultimate_system.add_charge(10)
            game_state.enemies_defeated += 1
            achievement_system.update_progress("enemies", 1)
            sound_event_bus.trigger_event("enemy_death")
            difficulty_system.increase_progression()

            if random.randint(0, 20) == 0:
                double_refill = DoubleRefill(
                    meteor2_object.rect.centerx,
                    meteor2_object.rect.centery,
                    double_refill_img,
                )
                double_refill_group.add(double_refill)

        if score >= 3000:
            meteor2_object.speed = 4
        if score >= 10000:
            meteor2_object.speed = 6
        if score >= 15000:
            meteor2_object.speed = 8
        if score >= 20000:
            meteor2_object.speed = 10

    # === ENEMY1 COMBAT SYSTEM ===
    for enemy_object in enemy1_group:
        if time_scale < 1.0:
            enemy_object.speed *= time_scale
            
        enemy_object.update(enemy1_group, enemy2_bullets)
        
        if time_scale < 1.0:
            enemy_object.speed /= time_scale

        if enemy_object.rect.colliderect(player.rect) and not dash_system.is_dashing:
            player_life -= 10
            damage_numbers.add(player.rect.centerx, player.rect.top, 10)
            explosion = Explosion(enemy_object.rect.center, explosion_images)
            explosions.add(explosion)
            enemy_object.kill()
            score += 20

        bullet_collisions = pygame.sprite.spritecollide(enemy_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion = Explosion(enemy_object.rect.center, explosion_images)
            explosions.add(explosion)
            enemy_object.kill()
            score += 50
            level_system.add_xp(30)
            ultimate_system.add_charge(25)
            game_state.enemies_defeated += 1
            achievement_system.update_progress("enemies", 1)
            sound_event_bus.trigger_event("enemy_death")
            difficulty_system.increase_progression()

            if random.randint(0, 8) == 0:
                bullet_refill = BulletRefill(
                    enemy_object.rect.centerx,
                    enemy_object.rect.centery,
                    bullet_refill_img,
                )
                bullet_refill_group.add(bullet_refill)

            if random.randint(0, 8) == 0:
                health_refill = HealthRefill(
                    random.randint(50, WIDTH - 30),
                    random.randint(-HEIGHT, -30),
                    health_refill_img,
                )
                health_refill_group.add(health_refill)

    # === ENEMY2 ADVANCED COMBAT SYSTEM ===
    for enemy2_object in enemy2_group:
        if time_scale < 1.0:
            enemy2_object.speed *= time_scale
            
        enemy2_object.update(enemy2_group, enemy2_bullets, player)
        
        if time_scale < 1.0:
            enemy2_object.speed /= time_scale

        if enemy2_object.rect.colliderect(player.rect) and not dash_system.is_dashing:
            player_life -= 40
            damage_numbers.add(player.rect.centerx, player.rect.top, 40)
            explosion2 = Explosion2(enemy2_object.rect.center, explosion2_images)
            explosions2.add(explosion2)
            enemy2_object.kill()
            score += 20

        bullet_collisions = pygame.sprite.spritecollide(enemy2_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion2 = Explosion2(enemy2_object.rect.center, explosion2_images)
            explosions2.add(explosion2)
            enemy2_object.kill()
            score += 80
            level_system.add_xp(50)
            ultimate_system.add_charge(35)
            game_state.enemies_defeated += 1
            achievement_system.update_progress("enemies", 1)
            sound_event_bus.trigger_event("enemy_death")
            difficulty_system.increase_progression()

            if random.randint(0, 20) == 0:
                double_refill = DoubleRefill(
                    enemy2_object.rect.centerx,
                    enemy2_object.rect.centery,
                    double_refill_img,
                )
                double_refill_group.add(double_refill)

    for enemy2_bullet in enemy2_bullets:
        if time_scale < 1.0:
            enemy2_bullet.speed *= time_scale

        if enemy2_bullet.rect.colliderect(player.rect) and not dash_system.is_dashing:
            player_life -= 10
            damage_numbers.add(player.rect.centerx, player.rect.top, 10)
            explosion = Explosion(player.rect.center, explosion3_images)
            explosions.add(explosion)
            enemy2_bullet.kill()

        if time_scale < 1.0:
            enemy2_bullet.speed /= time_scale

    enemy2_bullets.update()

    # === BOSS1 BATTLE SYSTEM ===
    for boss1_object in boss1_group:
        boss1_object.update(boss1_bullets, player)
        screen.blit(boss1_object.image, boss1_object.rect)
        boss1_bullets.update()
        boss1_bullets.draw(screen)

        if boss1_object.rect.colliderect(player.rect):
            player_life -= 20
            explosion = Explosion2(boss1_object.rect.center, explosion2_images)
            explosions2.add(explosion)

        bullet_collisions = pygame.sprite.spritecollide(boss1_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion2 = Explosion(boss1_object.rect.center, explosion2_images)
            explosions2.add(explosion2)
            damage = 5
            boss1_health -= damage
            damage_numbers.add(boss1_object.rect.centerx, boss1_object.rect.top, damage)
            
            if boss1_health <= 0:
                explosion = Explosion2(boss1_object.rect.center, explosion3_images)
                explosions.add(explosion)
                boss1_object.kill()
                score += 400
                level_system.add_xp(200)
                ultimate_system.add_charge(100)
                game_state.bosses_defeated += 1
                achievement_system.update_progress("bosses", 1)
                achievement_system.complete_special("boss_slayer")
                sound_event_bus.trigger_event("boss_death")

                if random.randint(0, 20) == 0:
                    double_refill = DoubleRefill(
                        boss1_object.rect.centerx,
                        boss1_object.rect.centery,
                        double_refill_img,
                    )
                    double_refill_group.add(double_refill)

        if boss1_health <= 0:
            explosion = Explosion2(boss1_object.rect.center, explosion2_images)
            explosions2.add(explosion)
            boss1_object.kill()

    for boss1_bullet in boss1_bullets:
        if boss1_bullet.rect.colliderect(player.rect) and not dash_system.is_dashing:
            player_life -= 20
            damage_numbers.add(player.rect.centerx, player.rect.top, 20)
            explosion = Explosion(player.rect.center, explosion3_images)
            explosions.add(explosion)
            boss1_bullet.kill()

    # === BOSS1 HEALTH BAR RENDERING ===
    if boss1_group:
        boss1_object = boss1_group.sprites()[0]
        boss1_health_bar_rect.center = (boss1_object.rect.centerx, boss1_object.rect.top - 5)
        pygame.draw.rect(screen, (255, 0, 0), boss1_health_bar_rect)
        pygame.draw.rect(screen, (0, 255, 0), (
            boss1_health_bar_rect.left,
            boss1_health_bar_rect.top,
            boss1_health,
            boss1_health_bar_rect.height
        ))

    # === BOSS2 BATTLE SYSTEM ===
    for boss2_object in boss2_group:
        boss2_object.update(boss2_bullets, player)
        screen.blit(boss2_object.image, boss2_object.rect)
        boss2_bullets.update()
        boss2_bullets.draw(screen)

        if boss2_object.rect.colliderect(player.rect):
            player_life -= 2
            explosion2 = Explosion2(boss2_object.rect.center, explosion2_images)
            explosions2.add(explosion2)

        bullet_collisions = pygame.sprite.spritecollide(boss2_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion2 = Explosion2(boss2_object.rect.center, explosion2_images)
            explosions2.add(explosion2)
            damage = 8
            boss2_health -= damage
            damage_numbers.add(boss2_object.rect.centerx, boss2_object.rect.top, damage)
            
            if boss2_health <= 0:
                explosion2 = Explosion2(boss2_object.rect.center, explosion3_images)
                explosions2.add(explosion2)
                boss2_object.kill()
                score += 800
                level_system.add_xp(400)
                ultimate_system.add_charge(150)
                game_state.bosses_defeated += 1
                achievement_system.update_progress("bosses", 1)
                achievement_system.complete_special("boss_slayer")
                sound_event_bus.trigger_event("boss_death")

                if random.randint(0, 20) == 0:
                    double_refill = DoubleRefill(
                        boss2_object.rect.centerx,
                        boss2_object.rect.centery,
                        double_refill_img,
                    )
                    double_refill_group.add(double_refill)

        if boss2_health <= 0:
            explosion = Explosion2(boss2_object.rect.center, explosion2_images)
            explosions2.add(explosion)
            boss2_object.kill()

    for boss2_bullet in boss2_bullets:
        if boss2_bullet.rect.colliderect(player.rect) and not dash_system.is_dashing:
            player_life -= 20
            damage_numbers.add(player.rect.centerx, player.rect.top, 20)
            explosion = Explosion(player.rect.center, explosion3_images)
            explosions.add(explosion)
            boss2_bullet.kill()

    # === BOSS2 HEALTH BAR RENDERING ===
    if boss2_group:
        boss2_object = boss2_group.sprites()[0]
        boss2_health_bar_rect.center = (boss2_object.rect.centerx, boss2_object.rect.top - 5)
        pygame.draw.rect(screen, (255, 0, 0), boss2_health_bar_rect)
        pygame.draw.rect(screen, (0, 255, 0), (
            boss2_health_bar_rect.left,
            boss2_health_bar_rect.top,
            boss2_health,
            boss2_health_bar_rect.height
        ))

    # === BOSS3 FINAL BOSS SYSTEM ===
    for boss3_object in boss3_group:
        boss3_object.update(boss3_bullets, player)
        screen.blit(boss3_object.image, boss3_object.rect)
        boss3_bullets.update()
        boss3_bullets.draw(screen)

        if boss3_object.rect.colliderect(player.rect):
            player_life -= 1
            explosion2 = Explosion2(boss3_object.rect.center, explosion2_images)
            explosions2.add(explosion2)

        bullet_collisions = pygame.sprite.spritecollide(boss3_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion2 = Explosion2(boss3_object.rect.center, explosion2_images)
            explosions2.add(explosion2)
            damage = 6
            boss3_health -= damage
            damage_numbers.add(boss3_object.rect.centerx, boss3_object.rect.top, damage)
            
            if boss3_health <= 0:
                explosion2 = Explosion2(boss3_object.rect.center, explosion3_images)
                explosions2.add(explosion2)
                boss3_object.kill()
                score += 1000
                level_system.add_xp(600)
                ultimate_system.add_charge(250)
                game_state.bosses_defeated += 1
                achievement_system.update_progress("bosses", 1)
                achievement_system.complete_special("champion")
                sound_event_bus.trigger_event("boss_death")

                if random.randint(0, 20) == 0:
                    double_refill = DoubleRefill(
                        boss3_object.rect.centerx,
                        boss3_object.rect.centery,
                        double_refill_img,
                    )
                    double_refill_group.add(double_refill)

        if boss3_health <= 0:
            explosion = Explosion2(boss3_object.rect.center, explosion2_images)
            explosions2.add(explosion)
            boss3_object.kill()

    for boss3_bullet in boss3_bullets:
        if boss3_bullet.rect.colliderect(player.rect) and not dash_system.is_dashing:
            player_life -= 20
            damage_numbers.add(player.rect.centerx, player.rect.top, 20)
            explosion = Explosion(player.rect.center, explosion3_images)
            explosions.add(explosion)
            boss3_bullet.kill()

    # === BOSS3 HEALTH BAR RENDERING ===
    if boss3_group:
        boss3_object = boss3_group.sprites()[0]
        boss3_health_bar_rect.center = (
            boss3_object.rect.centerx,
            boss3_object.rect.top - 5
        )
        pygame.draw.rect(screen, (255, 0, 0), boss3_health_bar_rect)
        pygame.draw.rect(screen, (0, 255, 0), (
            boss3_health_bar_rect.left,
            boss3_health_bar_rect.top,
            boss3_health,
            boss3_health_bar_rect.height)
        )

    # === PLAYER RENDERING ===
    enemy1_group.draw(screen)
    enemy2_group.draw(screen)
    enemy2_bullets.draw(screen)
    
    drone_manager.update(player.rect, bullets, Bullet)
    drone_manager.draw(screen)
    
    player_image_copy = player.image.copy()
    screen.blit(player_image_copy, player.rect)

# ████████████████████████████████████████████████████████████████████████████████
# ██                          RENDERING AND UI                                  ██
# ████████████████████████████████████████████████████████████████████████████████

# === VISUAL EFFECTS RENDERING ===
    for explosion in explosions:
        explosion.update()
        screen.blit(explosion.image, explosion.rect)

    for explosion2 in explosions2:
        explosion2.update()
        screen.blit(explosion2.image, explosion2.rect)

    for bullet in bullets:
        bullet.update()
        screen.blit(bullet.image, bullet.rect)

        if bullet.rect.bottom < 0:
            bullet.kill()
            bullet_counter -= 1

    # === MODERN UI UPDATE AND RENDERING ===
    dt = clock.get_time() / 1000.0 if clock.get_time() > 0 else 0.016
    
    health_bar.update(player_life, dt)
    score_display.score = score
    score_display.update(dt)
    particles.update(dt)
    effects_manager.update(int(dt * 1000))
    
    # Apply screen effects
    effected_surface = effects_manager.apply_effects(screen)
    screen.blit(effected_surface, (0, 0))
    
    # Draw modern UI components
    health_bar.draw(screen)
    score_display.draw(screen)
    particles.draw(screen)
    
    # Modern Feature UIs
    damage_numbers.update()
    damage_numbers.draw(screen)
    ultimate_system.draw_ui(screen, WIDTH, HEIGHT)
    level_system.draw_ui(screen, WIDTH)
    
    # Draw weapon and ammo info
    font_small = pygame.font.Font(None, 24)
    current_weapon = weapon_system.get_current_weapon()
    weapon_text = font_small.render(f"{current_weapon.name} | Ammo: {weapon_system.ammo}/{weapon_system.max_ammo}", True, (100, 200, 255))
    screen.blit(weapon_text, (WIDTH - 350, 50))

    # === DISPLAY UPDATE AND FRAME CONTROL ===
    pygame.display.flip()
    clock.tick(FPS)




# ████████████████████████████████████████████████████████████████████████████████
# ██                              CLEANUP                                       ██
# ████████████████████████████████████████████████████████████████████████████████

# === GAME CLEANUP AND EXIT ===
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
