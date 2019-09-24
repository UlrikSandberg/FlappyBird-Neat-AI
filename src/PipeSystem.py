import random

import pygame

from AABB import AABBPoint, AABB, aabbCollision


class PipeSystem:

    def __init__(self, pipeVelocity, spawnRate, screenWidth, screenHeight):
        self.pipeVelocity = pipeVelocity
        self.pipes = [Pipe(1, screenWidth, screenHeight)]
        self.spawnRate = spawnRate
        self.lastSpawned = 0
        self.numberOfSpawnedPipes = 1
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

    def process(self, deltaT):

        # Clean up pipes!
        for pipe in self.pipes:
            if pipe.x <= -60:
                self.pipes.remove(pipe)

        for pipe in self.pipes:
            pipe.x -= self.pipeVelocity * deltaT

    def pushPipe(self):
        self.numberOfSpawnedPipes += 1
        self.pipes.append(Pipe(self.numberOfSpawnedPipes, self.screenWidth, self.screenHeight))

    def getCurrentPipeIndexForX(self, x):

        for pipe in self.pipes:
            if pipe.x > x:
                return pipe

        return None

    def draw(self, screen):

        for pipe in self.pipes:
            pipe.draw(screen)

    def getPipes(self):
        return self.pipes

class Pipe:

    def __init__(self, pipeNr, screenWidth, screenHeight):

        self.pipeNr = pipeNr

        self.roofPipe = pygame.image.load("../imgs/roofpipe.png")
        self.floorPipe = pygame.image.load("../imgs/floorPipe.png")

        self.x = screenWidth

        self.screenHeight = screenHeight

        self.floorHeight = random.randrange(50, 350)
        self.roofHeight = screenHeight - 350 - self.floorHeight

        self.floorPipe = pygame.transform.scale(self.floorPipe, (60, self.floorHeight))
        self.roofPipe = pygame.transform.scale(self.roofPipe, (60, self.roofHeight))
        self.isPassed = False

    def draw(self, screen):
        screen.blit(self.roofPipe, (self.x, 0))
        screen.blit(self.floorPipe, (self.x, self.screenHeight - 150 - self.floorHeight))

    def getGapRoofY(self):
        return self.roofHeight

    def getGapFloorY(self):
        return self.screenHeight - 150 - self.floorHeight

    def getAABBs(self):
        return [AABB(self.x, 0, 60, self.roofHeight),
                AABB(self.x, self.screenHeight - 150 - self.floorHeight, 60, self.floorHeight)]

    def getPipeX(self):
        return self.x + 60

    def collide(self, bird):

        birdAABB = bird.getAABB()
        pipeAABBs = self.getAABBs()

        for aabb in pipeAABBs:
            if aabbCollision(aabb, birdAABB):
                return True
        return False


