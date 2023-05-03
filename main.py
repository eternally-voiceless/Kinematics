import pygame
import sys
from kinetic_tools import Particle, ViscousFluid, Background, restrict_area

pygame.init()

display_size = width, height = 1280, 610 #1280, 720
screen = pygame.display.set_mode(display_size)
clock = pygame.time.Clock()
dt = 0

test_particle_pos = (100, 100)
test_particle_velocity = (200, 200)
test_particle = Particle("./Planets/Planets/planet02.png", test_particle_pos, test_particle_velocity, 1_000, 0.1)

fluid = ViscousFluid(5.2)


back_layer_1 = Background("./Backgrounds/ground_frozen_ground_0059_01.jpg")
back_layer_1_pos = (10, screen.get_height()-back_layer_1.height-10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill("black") #"#6c757d"
    #back_layer_1.draw(screen)

    restrict_area(screen, test_particle)

    fluid.damping(test_particle, dt)
    test_particle.update(dt)
    test_particle.draw(screen)

    pygame.display.update()
    dt = clock.tick(60)/1000
