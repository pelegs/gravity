#!/usr/bin/env python3

from lib import *
import sys
import numpy as np

def print_3vec(vec):
    return '{:0.4f} {:0.4f} {:0.4f} '.format(vec[0], vec[1], vec[2])


star = body(np.zeros(3).astype(np.float64), np.zeros(3).astype(np.float64), 1E10, 'FF0000', R=10.0)
planet1 = body(np.array([140,0,0]).astype(np.float64), np.array([0,20,0]).astype(np.float64), 1E3, '0000ff', R=3.0)
planet2 = body(np.array([250,0,0]).astype(np.float64), np.array([0,10,0]).astype(np.float64), 1E2, '00ff00', R=2.0)
planet3 = body(np.array([50,0,0]).astype(np.float64), np.array([0,10,0]).astype(np.float64), 2E2, 'ff00aa', R=2.5)
comet   = body(np.array([400,0,0]).astype(np.float64), np.array([0,1,0]).astype(np.float64), 1E-3, 'ffffff', R=2.5)
system = [star, planet1, planet2, planet3, comet]

dt = 1E-6
G_univ = 200

# Make almost-circular orbits
v_y1 = np.sqrt(G_univ * star.mass / np.linalg.norm(planet1.pos - star.pos))
planet1.vel[1] = v_y1
v_y2 = np.sqrt(G_univ * star.mass / np.linalg.norm(planet2.pos - star.pos))
planet2.vel[1] = v_y2
v_y3 = np.sqrt(G_univ * star.mass / np.linalg.norm(planet3.pos - star.pos))
planet3.vel[1] = v_y3 * 0.9

# Make a lower eccentricity orbit for the comet
comet.vel[1] = 20000

pygame.init()
W, H, D = 800, 600, 0
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

    Ek = np.sum([b.Ek() for b in system])
    print('\rEk = {:0.5f}'.format(Ek), end='')
