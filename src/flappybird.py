import pygame
import neat
import os
import math

from Bird import Bird
from Environment import Environment
from PipeSystem import PipeSystem

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Initialize pygame framework
pygame.init()

font = pygame.font.SysFont("comicsans", 50)

Generation = 0

def main(genomes, config):
    # Count the number of generations
    global Generation
    Generation += 1

    birds = []  # <-- Hold all the birds!

    # Foreach genome from the neat framework create a bird and give it a brain
    for g_id, g in genomes:
        birds.append(Bird(200, 200, int(32 * 1.5), int(28 * 1.5), neat.nn.FeedForwardNetwork.create(g, config), g))

    # pygame display initialized
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Clock to control the framerate of the loop
    clock = pygame.time.Clock()

    # gameData
    gameSpeed = 300
    backgroundSpeed = 100
    pipeSpawnRate = 70
    score = 0

    # pipeSystem & Environment
    pipeSystem = PipeSystem(gameSpeed, pipeSpawnRate, SCREEN_WIDTH, SCREEN_HEIGHT)
    environment = Environment(gameSpeed, backgroundSpeed, SCREEN_WIDTH, SCREEN_HEIGHT)

    # game loop boolean to stop the simulation
    run = True
    while run:
        clock.tick(60)  # <-- Set the framerate to 60

        for event in pygame.event.get():  # <-- Check if the user closed the game
            if event.type == pygame.QUIT:
                run = False
                # Shuting down game
                pygame.quit()
                quit()
                break

        # Get bird_x, all the birds are moving equally quickly so they will be on the same x
        bird_x = birds[0].x
        # Get the upcomming pipe of interest
        upcomming_pipe = pipeSystem.getCurrentPipeIndexForX(bird_x)

        # Use the neural networks to move each bird!
        for x, bird in enumerate(birds):
            bird.process(0.0167)  # <--- Process each bird
            bird.reward(0.1); # <--- Rewards birds for surviving this many frames

            # Get output from the respective neural network controlling this bird
            # Inputs are the birds y, vertical distance to the roofPipe and vertical distance to the floor pipe, yVelocity, horizontal distance and the vector from the
            # birds lower right corner to the bottom pipe right upper corner
            if upcomming_pipe == None: # <--- If there is no upcomming pipe, set vertical distance to roof and floor
                output = bird.network.activate((bird.y,
                                           0,
                                           SCREEN_HEIGHT - 150,
                                           bird.velocity,
                                           1000))

            else: # <--- We have an upcomming bird give the bird appropriate input
                output = bird.network.activate((bird.y,
                                           abs(bird.y - upcomming_pipe.getGapRoofY()),
                                           abs(bird.y + bird.birdHeight - upcomming_pipe.getGapFloorY()),
                                           bird.velocity,
                                           upcomming_pipe.getPipeX() - bird.x))

            # if the output is greater than 0.5 make the bird jump
            if output[0] > 0.5:
                bird.jump()

            # Check if birds collide with the pipes, floor or roof
            if(collison(bird, pipeSystem.getPipes())):
                bird.reward(-1)
                birds.pop(x)

        if len(birds) < 1:
            run = False
            break

        pushNextPipe = False
        bird_x = birds[0].x

        for pipe in pipeSystem.getPipes(): # Traverse all the pipes and check if birds have passed
            if not pipe.isPassed:
                if pipe.x + 60 < bird_x:
                    pipe.isPassed = True # <--- Set pipe as passed
                    pushNextPipe = True # <--- Indicate that a new pipe should be spawned
                    score += 10 # <--- Visual score
                    for bird in birds: # <--- Reward all birds that have passed
                        bird.reward(5) # <--- Big reward for all birds passing pipes!!!

        if pushNextPipe:
            pipeSystem.pushPipe()

        environment.process(0.0167)
        pipeSystem.process(0.0167)

        environment.draw(screen)
        pipeSystem.draw(screen)

        for bird in birds:
            bird.draw(screen)

        # score
        score_label = font.render("Score: " + str(score), 1, (255, 255, 255))
        screen.blit(score_label, (SCREEN_WIDTH - score_label.get_width() - 15, 10))

        # generations
        generation_label = font.render("Generations: " + str(Generation), 1, (255, 255, 255))
        screen.blit(generation_label, (10, 10))

        # alive
        alive_label = font.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
        screen.blit(alive_label, (10, 50))

        pygame.display.update()

def collison(bird, pipes):

    for pipe in pipes:
        if pipe.collide(bird):
            return True
    if bird.y < 0:
        return True
    if bird.y + bird.birdHeight > 650:
        return True
    return False


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 100)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
