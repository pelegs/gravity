#!/usr/bin/env python3

from lib import *


def print_3vec(vec):
    return '{:0.4f} {:0.4f} {:0.4f} '.format(vec[0], vec[1], vec[2])


star = body(np.zeros(3).astype(np.float64), np.zeros(3).astype(np.float64), 1.0, 'FF0000')
planet = body(np.array([3,0,0]).astype(np.float64), np.array([0,0.01,0]).astype(np.float64), 1E-10, '0000FF')
system = [star, planet]

t_max = 10000
dt = 0.1

pygame.init()
W, H = 640, 480
center = np.array([W/2, H/2])
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
        b.move1(dt)
    #print('\r{:0.4f} '.format(t), print_3vec(planet.pos), print_3vec(star.pos), end='')
    for b in system:
        b.move2(dt, G=1E-3)

    # erase screen content
    screen.fill(black)

    # draw new stuff
    for b in system:
        b.draw(canvas, center)

    # update display
    pygame.display.update()
