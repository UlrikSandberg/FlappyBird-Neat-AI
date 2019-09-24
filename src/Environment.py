import pygame


class Environment:

    def __init__(self, baseVelocity, backgroundVelocity, screenWidth, screenHeight):

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        #Initialize backgrounds
        self.bg1 = Background(0, 0, self.screenWidth, self.screenHeight)
        self.bg2 = Background(self.screenWidth, 0, self.screenWidth, self.screenHeight)

        #Initialize base
        self.base1 = Base(0, self.screenHeight - 150, self.screenWidth, self.screenHeight)
        self.base2 = Base(self.screenWidth, self.screenHeight - 150, self.screenWidth, self.screenHeight)

        #Initialize background and base velocity
        self.baseVelocity = baseVelocity
        self.backgroundVelocity = backgroundVelocity

    def process(self, deltaT):

        # Paginating background
        self.bg1.x -= self.backgroundVelocity * deltaT
        self.bg2.x -= self.backgroundVelocity * deltaT

        if self.bg1.x <= -self.screenWidth:
            self.bg1.x = self.screenWidth

        if self.bg2.x <= -self.screenWidth:
            self.bg2.x = self.screenWidth

        # Paginating Base
        self.base1.x -= self.baseVelocity * deltaT
        self.base2.x -= self.baseVelocity * deltaT

        if self.base1.x <= -self.screenWidth:
            self.base1.x = self.screenWidth

        if self.base2.x <= -self.screenWidth:
            self.base2.x = self.screenWidth

    def draw(self, screen):

        self.bg1.draw(screen)
        self.bg2.draw(screen)

        self.base1.draw(screen)
        self.base2.draw(screen)

class Base:

    def __init__(self, x, y, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.base = pygame.image.load("../imgs/base.png")
        self.base = pygame.transform.scale(self.base, (self.screenWidth, 150))
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.base, (self.x, self.y))

class Background:

    def __init__(self, x, y, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.bg = pygame.image.load("../imgs/background.png")
        self.bg = pygame.transform.scale(self.bg, (self.screenWidth, self.screenHeight - 100))
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.bg, (self.x, self.y))