
"""
C = 6.67e-11 * 1.99e30

alpha = []
omega = [(C / (1.5e11 ** 3)) ** 0.5 * 1.3]
theta = [0]

ddr = []
dr = [1e4]
r = [1.5e11]

dt = 5000

for i in range(500000):
    alpha.append(-2 * omega[-1] * dr[-1] / r[-1])
    ddr.append(omega[-1] * omega[-1] * r[-1] - C / (r[-1] * r[-1]))

    omega.append(omega[-1] + alpha[-1] * dt)
    theta.append(theta[-1] + omega[-1] * dt)
    dr.append(dr[-1] + ddr[-1] * dt)
    r.append(r[-1] + dr[-1] * dt)

import matplotlib.pyplot as plt
from math import sin, cos

x, y = [R * cos(T) for R, T in zip(r, theta)], [R * sin(T) for R, T in zip(r, theta)]
plt.plot(x, y)
plt.plot(0, 0, 'ro')
plt.show()"""

import pygame as pg
import sys

from context import Context
import simulation
from vector import v2, v3

WIDTH, HEIGHT = 1200, 800
FPS = 60
BG_COLOUR = (30, 30, 30)

def main():

    # --- Initialization ---
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Antialiased Drawing with v2/v3")
    clock = pg.time.Clock()

    ctx = Context(screen, v2(WIDTH, HEIGHT), v2(0, 0), 5)

    pend = simulation.pendulum(0, (0, 0.4), (0, 0), (0, 0))
    pend.setParams()
    pend.run(10, 1 / 60)

    running = True
    i = 0
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(BG_COLOUR)

        pend.displayFrame(ctx, pend.h_Q[i], pend.h_dQ[i], pend.h_d2Q[i])

        pg.display.flip()

        i += 1
        i %= len(pend.h_T)

    pg.quit()

if __name__ == "__main__":
    main()