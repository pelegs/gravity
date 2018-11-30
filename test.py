#!/usr/bin/env python3

from lib import *
import sys
import numpy as np

def print_3vec(vec):
    return '{:0.4f} {:0.4f} {:0.4f} '.format(vec[0], vec[1], vec[2])


star = body(np.zeros(3).astype(np.float64), np.zeros(3).astype(np.float64), 1E10, 'FF0000', R=10.0)
planet = body(np.array([140,0,0]).astype(np.float64), np.array([0,20,0]).astype(np.float64), 1E3, '0000ff', R=3.0)
moon = body(np.array([143,0,0]).astype(np.float64), np.array([0,23,0]).astype(np.float64), 1e-10, 'ffffff')
system = [star, planet, moon]

dt = 1E-6
G_univ = 200

# Make circular orbit
v_y = np.sqrt(G_univ * star.mass / np.linalg.norm(planet.pos - star.pos))
planet.vel[1] = v_y
moon.vel[1] = v_y

pygame.init()
W, H, D = 640, 480, 0
center = np.array([W/2, H/2, D/2])
screen = pygame.display.set_mode ((W, H))

while True:
    # check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    # Dynamics
    for b in system:
        b.reset_neighbors()
        b.add_neighbors(system)
        b.temp_move(dt, G=G_univ)
    #print('\r{:0.4f} '.format(t), print_3vec(planet.pos), print_3vec(star.pos), end='')
    #for b in system:
    #    b.move2(dt, G=100000)

    # erase screen content
    screen.fill([0, 0, 0])

    # draw new stuff
    for b in system:
        b.draw(screen, center)

    # update display
    pygame.display.update()
