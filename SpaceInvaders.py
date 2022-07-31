import pygame
import random
import math
from pygame import mixer
import time

# initialize pygame
pygame.init()

# create screen
screenX = 800
screenY = 800
screen = pygame.display.set_mode( (screenX, screenY) )

# background
background = pygame.image.load("background.jpg")

#sounds
mixer.music.load('bgMusic.mp3')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Icon.jpg')
pygame.display.set_icon(icon)

# score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    global scoreValue
    score = font.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))



# player 
PlayerImage = pygame.image.load('SpaceShip.png')
PlayerImage = pygame.transform.scale(PlayerImage, (84, 84))
playerX = 370
playerY = 650
xChangePlayer = 0

def player(x, y):
    screen.blit(PlayerImage, (x, y))



# enemy 
EnemyImage = []
EnemyX = []
EnemyX_2 = [] # row bottom
EnemyY = []
EnemyY_2 = [] # row bottom
numEnemies = 4

for i in range(numEnemies):
    EnemyImage1 = pygame.image.load('enemy.png') 
    EnemyImage.append( pygame.transform.scale(EnemyImage1, (70, 70)) )
    y = i * 10
    x = y * 10
    EnemyX.append( x ) #150
    EnemyY.append(50)

    xEnemyChange = ( 0.2 )
    yEnemyChange = ( 40 )

for i in range(numEnemies):
    EnemyImage1 = pygame.image.load('enemy.png') 
    EnemyImage.append( pygame.transform.scale(EnemyImage1, (70, 70)) )
    y = i * 10
    x = y * 10
    EnemyX_2.append( x )
    EnemyY_2.append(150)

    xEnemyChange = ( 0.2 )
    yEnemyChange = ( 50 )

def enemy(x, x2, y, y2, i):
    screen.blit(EnemyImage[i], (x, y))
    screen.blit(EnemyImage[i], (x2, y2))

def enemyGameOver(x, x2, y, y2):
    screen.blit(EnemyImage[i], (x, y))
    screen.blit(EnemyImage[i], (x2, y2))


# bottom line
Line = pygame.image.load('BottomLine.jpg')
LineX = 0
LineY = 655

def BottomLine(x, y):
    global Line
    screen.blit(Line, (x, y))

# Laser 
LaserImage = pygame.image.load('PlayerLaser.png')
LaserImage = pygame.transform.scale(LaserImage, (50, 50))
LaserX = random.randint(15, (screenX - 85) ) 
LaserY = 750
xLaserChange = 0
yLaserChange = 1

# can't see bullet on screen until Ready changes to Fire
LaserState = "Ready"

def Firelaser(x, y):
    global LaserState
    LaserState = "Fire"
    screen.blit(LaserImage, (x+17, y+10))


# check collision
def Collision(EX, EX2, EY, EY2, LX, LY):
    distance = math.sqrt((math.pow(EX - LX, 2) + math.pow(EY - LY, 2)))
    distance2 = math.sqrt((math.pow(EX2 - LX, 2) + math.pow(EY2 - LY, 2)))

    if distance <= 35:
        return 1
    elif distance2 <= 35:
        return 2

        
def DistanceEnemy(EX, EX2, EY, EY2):
    distance = math.sqrt((math.pow(EX2 - EX, 2) + math.pow(EY2 - EY, 2)))

    if distance <= 70:
        return True


GameOverfont = pygame.font.Font('freesansbold.ttf', 82)

def GameOver():
    global GameOverfont
    text = GameOverfont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (140, 250))



# game loop
running = True
while running:

    # setting background
    screen.fill( (0, 0, 0) )
    screen.blit(background, (0, 0))


    # make function that closes program when x pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke detection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xChangePlayer = -0.4
            if event.key == pygame.K_RIGHT:
                xChangePlayer = +0.4
            if event.key == pygame.K_SPACE:
                if LaserState == "Ready":
                    LaserSound = mixer.Sound('shoot.wav')
                    LaserSound.play()
                    LaserX = playerX
                    LaserY = 600
                    Firelaser(LaserX, LaserY)
                    LaserY -= yLaserChange
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                xChangePlayer = 0


    # player movement 
    playerX += xChangePlayer

    # setting boudries for the player 
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 735

    # setting boudries for the enemy 
    for i in range(numEnemies):
        enemy(EnemyX[i], EnemyX_2[i], EnemyY[i], EnemyY_2[i], i)

        gameSoundPlayed = 0
        if EnemyY[i] >= 600 or EnemyY_2[i] >= 600 and (gameSoundPlayed == 0):
            GameOver()
            BottomLine(LineX, LineY)
            player(playerX, playerY)
            show_score(textX, textY)
            pygame.display.update()
            gameSoundPlayed += 1
            xEnemyChange = 0
            yEnemyChange = 0
            mixer.music.stop()
            mixer.music.load('GameOverSound.wav')
            mixer.music.play()
            time.sleep(3)
            break
            
            

        EnemyX[i] += xEnemyChange
        EnemyX_2[i] += xEnemyChange

        if EnemyX[i] >= 736 or EnemyX_2[i] >= 736:
            xEnemyChange = -0.2
            for x in range(len(EnemyY)):
                EnemyY[x] += yEnemyChange
            for x in range(len(EnemyY)):
                EnemyY_2[x] += yEnemyChange
        elif EnemyX[i] <= 0 or EnemyX_2[i] <= 0:
            xEnemyChange = 0.2
            for x in range(len(EnemyY)):
                EnemyY[x] += yEnemyChange
            for x in range(len(EnemyY)):
                EnemyY_2[x] += yEnemyChange
        

        # collision detection
        collision = Collision(EnemyX[i], EnemyX_2[i], EnemyY[i], EnemyY_2[i], LaserX, LaserY)
        if collision == 1:
            ExplosionSound = mixer.Sound('explosion.wav')
            ExplosionSound.play()
            LaserY = 600
            LaserState = "Ready"
            scoreValue += 1

            # enemy respawn
            OldEnemyY = EnemyY[i]
            EnemyY[i] = -20

            if EnemyY[i] >= OldEnemyY:
                EnemyY[i] -= 40

            EnemyDistance = DistanceEnemy(EnemyX[i], EnemyX_2[i], EnemyY[i], EnemyY_2[i])
            if EnemyDistance == True:
                EnemyY[i] -= 50


        if collision == 2:
            ExplosionSound = mixer.Sound('explosion.wav')
            ExplosionSound.play()
            LaserY = 600
            LaserState = "Ready"
            scoreValue += 1

            # enemy respawn row bottom
            OldEnemyY2 = EnemyY_2[i]
            EnemyY_2[i] = -40 

            if EnemyY_2[i] >= OldEnemyY2:
                EnemyY_2[i] -= 20

            EnemyDistance = DistanceEnemy(EnemyX[i], EnemyX_2[i], EnemyY[i], EnemyY_2[i])
            if EnemyDistance == True:
                EnemyY_2[i] -= 50

        enemy(EnemyX[i], EnemyX_2[i], EnemyY[i], EnemyY_2[i], i)


    # laser movement
    if LaserY <= -20:
        LaserY = 750
        LaserState = "Ready"

    if LaserState == "Fire":
        Firelaser(LaserX, LaserY)
        LaserY -= yLaserChange


    # outputting characters
    BottomLine(LineX, LineY)
    player(playerX, playerY)
    show_score(textX, textY)
    
    
    pygame.display.update()

    if gameSoundPlayed == 1:
        break