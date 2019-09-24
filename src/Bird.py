import pygame

from AABB import AABB

class Bird:

    def __init__(self, x, y, birdW, birdH, network, genome):
        self.IMGS = [pygame.transform.scale(pygame.image.load("../imgs/birdFrame1.png"), (birdW, birdH)), pygame.transform.scale(pygame.image.load("../imgs/birdFrame2.png"), (birdW, birdH)), pygame.transform.scale(pygame.image.load("../imgs/birdFrame3.png"), (birdW, birdH))]
        self.img = self.IMGS[0]
        self.x = x
        self.y = y
        self.velocity = 0
        self.acceleration = 0
        self.tick = 0
        self.animationTime = 5
        self.terminalVelocity = 1500
        self.maxAngle = 30
        self.currentAngle = 0
        self.angularVelocity = 200
        self.birdHeight = birdH
        self.birdWidth = birdW
        self.score = 0
        self.network = network
        self.genome = genome
        self.genome.fitness = 0

    def reward(self, reward):
        self.genome.fitness += reward

    def getAABB(self):
        return AABB(self.x, self.y, self.birdWidth, self.birdHeight)

    def jump(self):
        self.velocity = -500#-750

    def process(self, deltaT):

        self.velocity += self.acceleration * deltaT

        if self.velocity > self.terminalVelocity:
            self.velocity = self.terminalVelocity

        self.y += self.velocity * deltaT

        if self.velocity < 0:
            if self.currentAngle < self.maxAngle:
                self.currentAngle = self.maxAngle
            self.img = self.IMGS[1]
            self.tick = self.animationTime * 2
        else:
            if self.currentAngle > -90:
                self.currentAngle -= self.angularVelocity * deltaT

        self.acceleration = 2000#3711

    def draw(self, screen):

        self.tick += 1;

        if self.tick < self.animationTime:
            self.img = self.IMGS[0]
        elif self.tick < self.animationTime * 2:
            self.img = self.IMGS[1]
        elif self.tick < self.animationTime * 3:
            self.img = self.IMGS[2]
        elif self.tick < self.animationTime * 4:
            self.img = self.IMGS[1]
        elif self.tick < self.animationTime * 4 + 1:
            self.img = self.IMGS[0]
            self.tick = 0

        rotated_image = pygame.transform.rotate(self.img, self.currentAngle)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        screen.blit(rotated_image, new_rect.topleft)
