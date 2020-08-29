import math
import pygame
import random
from pygame import mixer
import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon_url = resource_path("Assets\\ufo.png")
icon = pygame.image.load(icon_url)
pygame.display.set_icon(icon)
background_url = resource_path("Assets\\background-1.png")
background = pygame.image.load(background_url)
music_url = resource_path("Assets\\background.wav")
mixer.music.load(music_url)
mixer.music.play(-1)

player_url = resource_path("Assets\\player.png")
playerImg = pygame.image.load(player_url)
playerX = 370
playerY = 480
playerX_change = 0
# playerY_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 25
for i in range(num_of_enemies):
    enemy_url = resource_path("Assets\\enemy-1.png")
    enemyImg.append(pygame.image.load(enemy_url))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(55, 150))
    enemyX_change.append(1)
    enemyY_change.append(30)

bullet_url = resource_path("Assets\\bullet.png")
bulletImg = pygame.image.load(bullet_url)
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
scoreX = 10
scoreY = 10

max_score_value = 0
# Under the current score:
max_scoreX = 10
max_scoreY = 50
# Top-right:
# max_scoreX = 575
# max_scoreY = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (200, 0, 0))
    screen.blit(over_text, (200, 250))

def show_max_score(x, y):
    save_file = open("max_score.txt", "r")
    max_score_value = int(save_file.read())
    max_score = font.render("Max score: " + str(max_score_value), True, (255, 255, 255))
    save_file.close()
    screen.blit(max_score, (x, y))

def player(x, y):
    screen.blit(playerImg, (int(x), y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (int(x), y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (int(x) + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    # distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 1.5
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    laser_url = resource_path("Assets\\laser.wav")
                    bullet_sound = mixer.Sound(laser_url)
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            """
            elif event.key == pygame.K_UP:
                playerY_change = -0.2
            elif event.key == pygame.K_DOWN:
                playerY_change = 0.2
            """
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            # elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            # playerY_change = 0

    playerX += playerX_change
    # playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # if playerY <= 0:
    #    playerY = 0
    # elif playerY >= 536:
    #    playerY = 536
    for i in range(num_of_enemies):
        if enemyY[i] >= 440:
            for j in range(num_of_enemies):
                enemyY[j] = 800
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.8
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.8
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound_url = resource_path("Assets\\explosion.wav")
            explosion_sound = mixer.Sound(explosion_sound_url)
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(55, 150)
        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    elif bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if("max_score.txt" not in os.listdir()):
        create_file = open("max_score.txt", "w")
        create_file.write("0")
        create_file.close()
    save_file = open("max_score.txt", "r")
    max_score_value = save_file.read()
    save_file.close()
    if score_value > int(max_score_value):
        save_file = open("max_score.txt", "w")
        save_file.write(str(score_value))
        save_file.close()
    player(playerX, playerY)
    show_score(scoreX, scoreY)
    show_max_score(max_scoreX, max_scoreY)
    pygame.display.update()
