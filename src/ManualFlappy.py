import pygame
import random
import numpy as np

from AABB import AABB, aabbCollision, AABBPoint
from Bird import Bird

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Deprecated manual flappy from early development
# Not currently working since refactor run flappybird.py for ai versioon
# Maybe this will be made into an Ai competition

class Environment:

    def __init__(self, baseVelocity, backgroundVelocity):

        #Initialize backgrounds
        self.bg1 = Background(0, 0)
        self.bg2 = Background(SCREEN_WIDTH, 0)

        #Initialize base
        self.base1 = Base(0, SCREEN_HEIGHT - 150)
        self.base2 = Base(SCREEN_WIDTH, SCREEN_HEIGHT - 150)

        #Initialize background and base velocity
        self.baseVelocity = baseVelocity
        self.backgroundVelocity = backgroundVelocity

    def process(self, deltaT):

        # Paginating background
        self.bg1.x -= self.backgroundVelocity * deltaT
        self.bg2.x -= self.backgroundVelocity * deltaT

        if self.bg1.x <= -SCREEN_WIDTH:
            self.bg1.x = SCREEN_WIDTH

        if self.bg2.x <= -SCREEN_WIDTH:
            self.bg2.x = SCREEN_WIDTH

        # Paginating Base
        self.base1.x -= self.baseVelocity * deltaT
        self.base2.x -= self.baseVelocity * deltaT

        if self.base1.x <= -SCREEN_WIDTH:
            self.base1.x = SCREEN_WIDTH

        if self.base2.x <= -SCREEN_WIDTH:
            self.base2.x = SCREEN_WIDTH

    def draw(self, screen):

        self.bg1.draw(screen)
        self.bg2.draw(screen)

        self.base1.draw(screen)
        self.base2.draw(screen)

class Base:

    def __init__(self, x, y):
        self.base = pygame.image.load("../imgs/base.png")
        self.base = pygame.transform.scale(self.base, (SCREEN_WIDTH, 150))
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.base, (self.x, self.y))

class Background:

    def __init__(self, x, y):
        self.bg = pygame.image.load("../imgs/background.png")
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT - 100))
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.bg, (self.x, self.y))

class PipeSystem:

    def __init__(self, pipeVelocity, spawnRate):
        self.pipeVelocity = pipeVelocity
        self.pipes = []
        self.spawnRate = spawnRate
        self.lastSpawned = 70
        self.numberOfSpawnedPipes = 1

    def process(self, deltaT):

        self.lastSpawned += 1

        if self.lastSpawned > self.spawnRate:
            self.pipes.append(Pipe(self.numberOfSpawnedPipes))
            self.numberOfSpawnedPipes += 1
            self.lastSpawned = 0

            for pipe in self.pipes:
                if pipe.x <= -60:
                    self.pipes.remove(pipe)

        for pipe in self.pipes:
            pipe.x -= self.pipeVelocity * deltaT

    def draw(self, screen):

        for pipe in self.pipes:
            pipe.draw(screen)

    def getPipes(self):
        return self.pipes

class Pipe:

    def __init__(self, pipeNr):
        self.pipeNr = pipeNr
        self.roofPipe = pygame.image.load("../imgs/roofpipe.png")
        self.floorPipe = pygame.image.load("../imgs/floorPipe.png")

        self.x = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        self.floorHeight = random.randrange(50, 350)
        self.roofHeight = SCREEN_HEIGHT - 350 - self.floorHeight

        self.floorPipe = pygame.transform.scale(self.floorPipe, (60, self.floorHeight))
        self.roofPipe = pygame.transform.scale(self.roofPipe, (60, self.roofHeight))

    def getPipeGate(self):
        return AABBPoint(self.x + 60 , self.roofHeight, 30, SCREEN_HEIGHT - 200 - self.floorHeight - self.roofHeight, self.pipeNr)

    def draw(self, screen):

        screen.blit(self.roofPipe, (self.x, 0))
        screen.blit(self.floorPipe, (self.x, self.height - 150 - self.floorHeight))


    def getAABB(self):

        floorAABB = AABB(self.x, self.height - 150 - self.floorHeight, 60, self.floorHeight)
        roofAABB = AABB(self.x, 0, 60, self.roofHeight)

        return floorAABB, roofAABB

def detectCollision(pipeSystem, bird, floorHeight):

    # Check for collision with the floor
    if bird.y + bird.birdHeight > floorHeight:
        bird.y = floorHeight - bird.birdHeight
        return True

    # Check for collision with the roof
    if bird.y < 0:
        bird.y = 0
        return True

    # Get bird AABB
    birdAABB = bird.getAABB()

    # Iterate all the pipes on screen
    for pipe in pipeSystem.getPipes():

        # Check if bird is colliding with checkpoint
        if aabbCollision(birdAABB, pipe.getPipeGate()):
            if bird.score < pipe.getPipeGate().pipeNr * 10:
                bird.score += 10
                return False

        # For each pipe get floor and roof pipes and check for collision against birdAABB
        for pipeAABB in pipe.getAABB():
            if aabbCollision(pipeAABB, birdAABB):
                return True

    # no collison thus return false
    return False

class GameEntities:

    def __init__(self, gameSpeed, spawnRate):
        self.bird = Bird(200, 200, int(32*1.5), int(28*1.5))
        self.environment = Environment(gameSpeed, 100)
        self.pipeSystem = PipeSystem(gameSpeed, spawnRate);

    def process(self, deltaT, screen, paused, jump):

        if paused:
            self.draw(screen)
        else:
            self.environment.process(deltaT)
            self.pipeSystem.process(deltaT)
            if jump:
                self.bird.jump()
            self.bird.process(deltaT)

            self.draw(screen)

    def draw(self, screen):
        self.environment.draw(screen)
        self.pipeSystem.draw(screen)
        self.bird.draw(screen)


def mainLoop():
    # Define a pygame window...
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 25)

    jump = False
    dead = False
    paused = True

    spacePressed = False

    gameSpeed = 300
    spawnRate = 70

    gameEntities = GameEntities(gameSpeed, spawnRate)

    # Initializes a game clock to run the game loop for a certain amount of time
    clock = pygame.time.Clock()

    # Game loop boolean
    run = True

    # Run the game loop
    while run:

        clock.tick(60)  # <-- Only run game loop 60 times a second

        # Check for input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    spacePressed = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not spacePressed:
                    spacePressed = True
                    jump = True
                    paused = False

        gameEntities.process(0.0167, screen, paused, jump)

        screen.blit(font.render("Score: " + str(gameEntities.bird.score), True, (255, 255, 255)), (10, 10))

        jump = False

        if detectCollision(gameEntities.pipeSystem, gameEntities.bird, 650):
            dead = True

        if dead: # Reset game!
            gameEntities = GameEntities(gameSpeed, spawnRate)
            paused = False
            dead = False
            jump = False
            last_distance = 10000
            distance = 0

        pygame.display.update()

def main():

    pygame.init()

    runGame = True

    while runGame:

        mainLoop()

    # Shuting down game
    pygame.quit()
    quit()


main()