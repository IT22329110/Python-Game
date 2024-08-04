import pygame
import random
import math

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('startup.png')
pygame.display.set_icon(icon)

# Player
playerIMG = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# UFO
ufoIMG = []
ufoX = []
ufoY = []
ufoX_change = []
ufoY_change = []
num_of_ufo = 6

for i in range(num_of_ufo):
    ufoIMG.append(pygame.image.load('ufo.png'))
    ufoX.append(random.randint(0, 736))
    ufoY.append(random.randint(50, 150))
    ufoX_change.append(0.3)
    ufoY_change.append(40)  # Change UFO's Y position when hitting the screen edges

# Bullet
warIMG = pygame.image.load('war.png')
warX = 0
warY = 480
warX_change = 0
warY_change = 2  # Decreased bullet speed
war_state = "ready"

# Score
score = 0

def player(x, y):
    screen.blit(playerIMG, (x, y))

def ufo(x, y, i):
    screen.blit(ufoIMG[i], (x, y))

def fire_war(x, y):
    global war_state
    war_state = "fire"
    screen.blit(warIMG, (x + 16, y + 10))

def isCollision(ufoX, ufoY, warX, warY):
    distance = math.sqrt((math.pow(ufoX - warX, 2)) + (math.pow(ufoY - warY, 2)))
    return distance < 27

# Game loop
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke is pressed check whether right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if war_state == "ready":
                    warX = playerX
                    fire_war(warX, warY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Update player position
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # UFO movement
    for i in range(num_of_ufo):
        ufoX[i] += ufoX_change[i]
        if ufoX[i] <= 0:
            ufoX_change[i] = 0.3
            ufoY[i] += ufoY_change[i]
        elif ufoX[i] >= 736:
            ufoX_change[i] = -0.3
            ufoY[i] += ufoY_change[i]

        # Collision
        collision = isCollision(ufoX[i], ufoY[i], warX, warY)
        if collision:
            warY = 480
            war_state = "ready"
            score += 1
            print(score)
            ufoX[i] = random.randint(0, 736)
            ufoY[i] = random.randint(50, 150)

        ufo(ufoX[i], ufoY[i], i)

    # Bullet movement
    if warY <= 0:
        warY = 480
        war_state = "ready"

    if war_state == "fire":
        fire_war(warX, warY)
        warY -= warY_change

    # Draw the player
    player(playerX, playerY)

    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()
