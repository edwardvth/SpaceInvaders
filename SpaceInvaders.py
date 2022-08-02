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


GameOverfont = pygame.font.Font('freesansbold.ttf', 82)

def GameOver():
    global GameOverfont
    text = GameOverfont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (140, 250))





# enemy
class EnemyClass:
    EnemyImage = pygame.transform.scale(pygame.image.load('enemy.png'), (70, 70))

    def __init__(self):
        self.EnemyX = []
        self.EnemyY = []
        self.numEnemies = 4
        self.xEnemyChange = 0.2
        self.yEnemyChange = 50

        
    def enemyMovement(self, i):
        self.EnemyX[i] += self.xEnemyChange

        if self.EnemyX[i] >= 736:
            self.xEnemyChange = -self.xEnemyChange
            for x in range(len(self.EnemyY)):
                self.EnemyY[x] += self.yEnemyChange
        elif self.EnemyX[i] <= 0:
            self.xEnemyChange = .2
            for x in range(len(self.EnemyY)):
                self.EnemyY[x] += self.yEnemyChange

    def enemy(self, i):
        screen.blit(EnemyClass.EnemyImage, (self.EnemyX[i], self.EnemyY[i]))

    def enemyGameOver(self, x, y):
        screen.blit(EnemyClass.EnemyImage[i], (x, y))

    def CollisionDetection(self, i, scoreValue, lasery, laserstate):
        global LaserY, LaserState
        ExplosionSound = mixer.Sound('explosion.wav')
        ExplosionSound.play()
        LaserY = lasery
        LaserState = laserstate
        scoreValue += 1

        # enemy respawn
        OldEnemyY = self.EnemyY[i]
        self.EnemyY[i] = -20

        if self.EnemyY[i] >= OldEnemyY:
            self.EnemyY[i] -= 40



EnemyRowBottom = EnemyClass()
EnemyRowTop = EnemyClass()

for i in range(EnemyRowBottom.numEnemies):
    y = i * 10
    x = y * 10
    EnemyRowBottom.EnemyX.append( x ) 
    EnemyRowBottom.EnemyY.append( 150 )

for i in range(EnemyRowTop.numEnemies):
    y = i * 10
    x = y * 10
    EnemyRowTop.EnemyX.append( x ) 
    EnemyRowTop.EnemyY.append( 50 )





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
    for i in range(EnemyRowTop.numEnemies):

        BlitEnemy1 = EnemyRowTop.enemy(i)
        BlitEnemy2 = EnemyRowBottom.enemy(i)

        gameSoundPlayed = 0
        if EnemyRowTop.EnemyY[i] >= 600 or EnemyRowBottom.EnemyY[i] >= 600 and (gameSoundPlayed == 0):
            GameOver()
            BottomLine(LineX, LineY)
            player(playerX, playerY)
            show_score(textX, textY)
            pygame.display.update()
            gameSoundPlayed += 1
            EnemyRowTop.xEnemyChange = 0
            EnemyRowTop.yEnemyChange = 0
            EnemyRowBottom.xEnemyChange = 0
            EnemyRowBottom.yEnemyChange = 0
            mixer.music.stop()
            mixer.music.load('GameOverSound.wav')
            mixer.music.play()
            time.sleep(3)
            break

            
        EnemyRowTop.enemyMovement(i)
        EnemyRowBottom.enemyMovement(i)        


        # collision detection
        collision = Collision(EnemyRowTop.EnemyX[i], EnemyRowBottom.EnemyX[i], EnemyRowTop.EnemyY[i], EnemyRowBottom.EnemyY[i], LaserX, LaserY)
        if collision == 1:
            EnemyRowTop.CollisionDetection(i, scoreValue, 600, "Ready")

            EnemyDistance = DistanceEnemy(EnemyRowTop.EnemyX[i], EnemyRowBottom.EnemyX[i], EnemyRowTop.EnemyY[i], EnemyRowBottom.EnemyY[i])
            if EnemyDistance == True:
                EnemyRowTop.EnemyY[i] -= 50



        if collision == 2:
            EnemyRowBottom.CollisionDetection(i, scoreValue, 600, "Ready")

            EnemyDistance = DistanceEnemy(EnemyRowTop.EnemyX[i], EnemyRowBottom.EnemyX[i], EnemyRowTop.EnemyY[i], EnemyRowBottom.EnemyY[i])
            if EnemyDistance == True:
                EnemyRowBottom.EnemyY[i] -= 50

        BlitEnemy1
        BlitEnemy2


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
