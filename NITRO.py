import random
import sys
import pygame
from pygame import *

FPS = 32
SCREEN_WIDTH = 300  # In pixels
SCREEN_HEIGHT = 500  # In pixels
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # For displaying screen
GAME_SPRITES = {}
GAME_SOUNDS = {}
X = [22, 113, 211]  # Lane's x coordinates
OFFSET = 300  # Minimum gap between each obstacles
PLAYER = 'Sprites/Player.png'
BACKGROUND = 'Sprites/Road.png'
OBS = ['Sprites/Obstacle1.png', 'Sprites/Obstacle2.png']


def welcomeScreen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['open screen'], (0, 0))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = 113
    playery = SCREEN_HEIGHT - GAME_SPRITES['player'].get_height()

    # Generating two cars at most on the screen.
    car1 = randomObstacles()
    car2 = randomObstacles()

    # Velocity of obstacles[cars]. Can be increased or decreased within range for difficulty level.
    obstacleVelY = 8

    # Velocity of road.
    roadVel = 3

    # List of road.
    roads = [{'x': 0, 'y': 0}, {'x': 0, 'y': -500}]

    # List of two cars
    cars = [{'t': car1[0]['t'], 'x': car1[0]['x'], 'y': -40},
            {'t': car2[0]['t'], 'x': car2[0]['x'], 'y': -40 - OFFSET}
            ]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Changing lanes
            if event.type == KEYDOWN and event.key == K_LEFT:
                if playerx == 113:
                    playerx = 22
                elif playerx == 211:
                    playerx = 113
                elif playerx == 22:
                    playerx = 22

            elif event.type == KEYDOWN and event.key == K_RIGHT:
                if playerx == 113:
                    playerx = 211
                elif playerx == 211:
                    playerx = 211
                elif playerx == 22:
                    playerx = 113

        # Crash test check
        if crashTest(cars, playerx, playery):
            SCREEN.blit(GAME_SPRITES['fire'], (cars[0]['x'], cars[0]['y']))
            GAME_SOUNDS['music'].stop()
            GAME_SOUNDS['crash'].play()
            return

        else:
            # When cars are about to disappear from the screen.
            if 490 < (cars[0]['y']) < 500:
                newCar = randomObstacles()
                cars.append(newCar[0])

            # When cars disappear from the screen, pop the first item of list and increase score by 1.
            if (cars[0]['y']) > 500:
                cars.pop(0)
                score += 1
                # print(f"Your score is {score}")

            # When road is about to disappear from the screen.
            if 480 < (roads[0]['y']):
                roads.append({'x': 0, 'y': roads[1]['y'] - 500})

            # When road disappears from the screen, pop the first item of roads list.
            if (roads[0]['y']) >= 500:
                roads.pop(0)

            # Move obstacles with a velocity in y direction.
            for item in cars:
                item['y'] += obstacleVelY

            # Move road with a velocity in y direction.
            for road in roads:
                road['y'] += roadVel

            # Blit roads and obstacles on screen.
            for road in roads:
                SCREEN.blit(GAME_SPRITES['background'], (0, road['y']))
            for item in cars:
                SCREEN.blit(item['t'], (item['x'], item['y']))

            SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

            # For printing score
            digits = [int(x) for x in list(str(score))]
            width = 0
            for digit in digits:
                width += GAME_SPRITES['score'][digit].get_width()
            XPos = (SCREEN_WIDTH - width) / 2

            for digit in digits:
                SCREEN.blit(GAME_SPRITES['score'][digit], (XPos, SCREEN_HEIGHT * 0.02))
                XPos += GAME_SPRITES['score'][digit].get_width()

            GAME_SOUNDS['music'].play()

            pygame.display.update()
            FPSCLOCK.tick(FPS)


# Crash test
def crashTest(cars, playerx, playery):
    for items in cars:
        if items['x'] == playerx and playery < items['y'] and items['y'] - playery < GAME_SPRITES[
            'player'].get_height():
            return True
        elif items['x'] == playerx and playery > items['y'] and playery - items['y'] < GAME_SPRITES[
            'player'].get_height():
            return True

        return False


# Generating random obstacles[cars] in random lanes.
def randomObstacles():
    obstacleChoice = random.choice(GAME_SPRITES['obstacles'])
    obstaclex = random.choice(X)
    obstacley = 80
    obstacle = [{'t': obstacleChoice, 'x': obstaclex, 'y': -obstacley}]

    return obstacle


# Game over Screen
def gameOverScreen():
    SCREEN.blit(GAME_SPRITES['game over'], (90, 100))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return


if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Nitro Race")

    GAME_SPRITES['player'] = pygame.image.load('Sprites/Player.png').convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load('Sprites/Road.png').convert_alpha()
    GAME_SPRITES['obstacles'] = (
        pygame.image.load('Sprites/Obstacle1.png').convert_alpha(),
        pygame.image.load('Sprites/Obstacle2.png').convert_alpha(),
        pygame.image.load('Sprites/Obstacle3.png').convert_alpha(),
        pygame.image.load('Sprites/Obstacle4.png').convert_alpha(),
        pygame.image.load('Sprites/Obstacle5.png').convert_alpha(),
    )

    GAME_SPRITES['open screen'] = pygame.image.load('Sprites/Welcome.png').convert_alpha()
    GAME_SPRITES['game over'] = pygame.image.load('Sprites/Game Over.png').convert_alpha()
    GAME_SPRITES['fire'] = pygame.image.load('Sprites/Fire.png').convert_alpha()

    GAME_SPRITES['score'] = (
        pygame.image.load('Sprites/0.png').convert_alpha(),  # Convert alpha--> do fast rendering of images.
        pygame.image.load('Sprites/1.png').convert_alpha(),
        pygame.image.load('Sprites/2.png').convert_alpha(),
        pygame.image.load('Sprites/3.png').convert_alpha(),
        pygame.image.load('Sprites/4.png').convert_alpha(),
        pygame.image.load('Sprites/5.png').convert_alpha(),
        pygame.image.load('Sprites/6.png').convert_alpha(),
        pygame.image.load('Sprites/7.png').convert_alpha(),
        pygame.image.load('Sprites/8.png').convert_alpha(),
        pygame.image.load('Sprites/9.png').convert_alpha(),
    )

    GAME_SOUNDS['music'] = pygame.mixer.Sound('Sounds/Music.wav')
    GAME_SOUNDS['crash'] = pygame.mixer.Sound('Sounds/Crash.wav')

    while True:
        welcomeScreen()
        mainGame()
        gameOverScreen()
