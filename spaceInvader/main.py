import pygame
import random
import math
import time
from pygame import mixer
pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('background.png')

pygame.display.set_caption("Robo Spader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerImage = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change = 4
enemyY_change = 16


bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


mixer.music.load("background.wav")
mixer.music.play(-1)


def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) +
                         (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


running = True

while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_LEFT:
                playerX_change -= 15
            elif event.key == pygame.K_RIGHT:
                playerX_change += 15
            elif event.key == pygame.K_UP:
                playerY_change -= 15
            elif event.key == pygame.K_DOWN:
                playerY_change += 15
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_SPACE:
                bulletX = playerX+playerX_change
                bulletY = playerY+playerY_change
                fire_bullet(bulletX, bulletY)
    if playerX_change <= -370:
        playerX_change = -370
    elif playerX_change >= 370:
        playerX_change = 370

    enemyX += enemyX_change
    if(enemyX > 736):
        enemyX_change = -enemyX_change
        enemyY += enemyY_change
    elif(enemyX < 0):
        enemyX_change = -enemyX_change
        enemyY += enemyY_change

    if(enemyY > 400):
        game_over_text()
        pygame.display.update()
        time.sleep(2)
        break

    if(bullet_state == "fire"):
        fire_bullet(bulletX, bulletY)
        bulletY = bulletY-bulletY_change
        if(bulletY < 0):
            bullet_state == "ready"

    if(isCollision(enemyX, enemyY, bulletX, bulletY)):
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)
        bullet_state == "ready"
        score_value += 1

    player(playerX+playerX_change, playerY+playerY_change)
    enemy(enemyX, enemyY)
    show_score(20, 20)
    pygame.display.update()
