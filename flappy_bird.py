import pygame
import sys
import random


def drawGround():
    screen.blit(ground, (groundXPos, 400))
    screen.blit(ground, (groundXPos + 288, 400))


def createPipe():
    pipeHeight = random.randint(150, 275)
    gapBetweenPipes = random.randint(80, 150)
    pipeTopHeight = pipeHeight-gapBetweenPipes
    pipeBottom = pipeSurfaceGreen.get_rect(midtop=(300, pipeHeight))
    pipetop = pipeSurfaceGreen.get_rect(midbottom=(300, pipeTopHeight))
    return pipeBottom, pipetop


def movePipeLeft(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def drawPipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 470:
            screen.blit(pipeSurfaceGreen, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipeSurfaceGreen, False, True)
            screen.blit(flip_pipe, pipe)


def checkCollide(pipes):
    for pipe in pipes:
        if rectBird.colliderect(pipe):
            return False
    if rectBird.top <= -100 or rectBird.bottom >= 400:
        return False
    return True


def rotateBird(bird):
    new_bird = pygame.transform.rotozoom(bird, -birdDisplacement*5, 1)
    return new_bird


def animateBird():
    new_bird = birdFrameList[birdDisplay]
    new_rectBird = new_bird.get_rect(center=(100, rectBird.centery))
    return new_bird, new_rectBird


def scoreDisplay(currentGameState):
    if currentGameState == 'mainGame':
        surfaceScore = game_font.render(str(int(score)), True, (255, 255, 255))
        rectScore = surfaceScore.get_rect(center=(144, 30))
        screen.blit(surfaceScore, rectScore)
    if currentGameState == 'gameOver':
        play_again = pygame.font.Font('./sprites/Game_Font.ttf', 20)
        surfaceScore = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
        rectScore = surfaceScore.get_rect(center=(144, 200))
        screen.blit(surfaceScore, rectScore)

        surfaceHighScore = game_font.render(f'High-score:{int(highScore)}', True, (255, 255, 255))
        rectHighScore = surfaceHighScore.get_rect(center=(144, 230))
        playAgainOption = play_again.render(f'Press Space to play again!', True, (255, 255, 255))
        rectPlayAgain = surfaceHighScore.get_rect(center=(110, 265))
        screen.blit(surfaceHighScore, rectHighScore)
        screen.blit(playAgainOption, rectPlayAgain)


def newScore(displayedScore, displayedHighScore):
    if displayedScore > displayedHighScore:
        displayedHighScore = displayedScore
    return displayedHighScore


pygame.init()
screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

gravity = 0.16
birdDisplacement = 0

backgroundDay = pygame.image.load("./sprites/background-day.png").convert()
backgroundNight = pygame.image.load("./sprites/background-night.png").convert()
ground = pygame.image.load("./sprites/base.png").convert()
groundXPos = 0

birdFrameList = [
    pygame.image.load("./sprites/bluebird-downflap.png").convert_alpha(),
    pygame.image.load("./sprites/bluebird-midflap.png").convert_alpha(), 
    pygame.image.load("./sprites/bluebird-upflap.png").convert_alpha(),
    pygame.image.load("./sprites/bluebird-midflap.png").convert_alpha()
]
birdDisplay = 1
birdSurface = birdFrameList[birdDisplay]
pygame.display.set_icon( pygame.image.load("./sprites/redbird-midflap.png").convert_alpha() )
rectBird = birdSurface.get_rect(center=(100, 206))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipeSurfaceGreen = pygame.image.load("./sprites/pipe-green.png").convert()
pipeList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 800)
game_font = pygame.font.Font('./sprites/Game_Font.ttf', 30)

isGameActive = checkCollide(pipeList)
score = 0
highScore = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                birdDisplacement = 0
                birdDisplacement -= 5
            if event.key == pygame.K_SPACE and not isGameActive:
                isGameActive = True
                pipeList.clear()
                rectBird.center = (100, 206)
                score = 0
        if event.type == SPAWNPIPE:
            pipeList.extend(createPipe())
        if event.type == BIRDFLAP:
            if birdDisplay < 3:
                birdDisplay += 1
            else:
                birdDisplay = 0
    birdSurface, rectBird = animateBird()
    screen.blit(backgroundDay, (0, 0))
    if isGameActive:

        birdDisplacement += gravity
        rotated_bird = rotateBird(birdSurface)
        screen.blit(rotated_bird, rectBird)

        pipeList = movePipeLeft(pipeList)
        drawPipe(pipeList)
        score += 0.01
        scoreDisplay('mainGame')
        isGameActive = checkCollide(pipeList)
        groundXPos -= 1
    else:
        highScore = newScore(score, highScore)
        scoreDisplay('gameOver')

    if groundXPos <= -288:
        groundXPos = 0
    rectBird.centery += birdDisplacement
    drawGround()
    pygame.display.update()
    clock.tick(120)
