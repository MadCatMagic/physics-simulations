
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

from math import *
import pygame as pg
import pygame.gfxdraw as gfxdraw

class Context:
    def __init__(self, screen, screenSize, centre, size):
        self.screen = screen
        self.centre = (centre[0] - size * 0.5, centre[1] - size * screenSize[1] / screenSize[0] * 0.5)
        self.size = size
        self.screenSize = screenSize

        self.col = (255, 255, 255)

    def transform(self, p):
        return (
            int((p[0] - self.centre[0]) / self.size * self.screenSize[0]), 
            int(self.screenSize[1] - (p[1] - self.centre[1]) / self.size * self.screenSize[0])
        )

    def line(self, p1, p2):
        gfxdraw.line(self.screen, *self.transform(p1), *self.transform(p2), self.col)

    def rect(self, centre, size):
        c = self.transform((centre[0] - size[0], centre[1] + size[1]))
        hs = (
            int(size[0] / self.size * self.screenSize[0]), 
            int(size[1] / self.size * self.screenSize[0])
        )
        #pg.gfxdraw.aacircle(self.screen, c[0], c[1], , color.to_color_tuple())
        #pg.gfxdraw.filled_circle(self.screen, int(center.x), int(center.y), radius, color.to_color_tuple())

        pg.draw.rect(self.screen, self.col, (c[0], c[1], hs[0] * 2, hs[1] * 2), 0)

    def circle(self, centre, radius):
        c = self.transform(centre)
        r = int(radius / self.size * self.screenSize[0])
        gfxdraw.aacircle(self.screen, c[0], c[1], r, self.col)
        gfxdraw.filled_circle(self.screen, c[0], c[1], r, self.col)

class Sim:
    def __init__(self, t0, q0: tuple, d_q0: tuple, d2_q0: tuple):
        # current values
        self.t = t0
        self.q: tuple = q0
        self.d_q: tuple = d_q0
        self.d2_q: tuple = d2_q0
        # history variables
        self.h_T = [t0]
        self.h_Q: list[tuple] = [q0]
        self.h_dQ: list[tuple] = [d_q0]
        self.h_d2Q: list[tuple] = [d2_q0]

    def setd2s(self):
        raise NotImplementedError()
    
    def displayFrame(self, ctx, q, d_q, d2_q):
        raise NotImplementedError()
    
    def update(self, dt):
        self.setd2s()
        self.d_q = tuple(map(lambda x: x[0] + x[1] * dt, zip(self.d_q, self.d2_q)))
        self.q = tuple(map(lambda x: x[0] + x[1] * dt, zip(self.q, self.d_q)))

        self.t += dt

        self.h_T.append(self.t)
        self.h_Q.append(self.q)
        self.h_dQ.append(self.d_q)
        self.h_d2Q.append(self.d2_q)

    def run(self, duration, dt):
        t0 = self.t
        while self.t - t0 < duration:
            self.update(dt)

# q = (x, theta)
class pendulum(Sim):
    def setParams(self):
        self.m = 1
        self.M = 2
        self.l = 0.5
        self.g = -9.81

    def setd2s(self):
        theta = self.q[1]
        d_theta = self.d_q[1]
        tdd = (self.m * self.l * d_theta ** 2 * sin(theta) * cos(theta) - (self.m + self.M) * self.g * sin(theta)) / (self.m * self.l * cos(theta) ** 2 - (self.m + self.M) * self.l)
        self.d2_q = (
            self.g * tan(theta) - self.l * tdd / cos(theta),
            tdd
        )

    def displayFrame(self, ctx, q, d_q, d2_q):
        ctx.col = (200, 200, 200)
        ctx.line((-5, 0), (5, 0))
        ctx.col = (255, 255, 255)
        ctx.rect((q[0], 0.1), (0.1, 0.1))
        ctx.line((q[0], 0), (q[0] + self.l * sin(q[1]), -self.l * cos(q[1])))
        ctx.circle((q[0] + self.l * sin(q[1]), -self.l * cos(q[1])), 0.1)

# --- Main Loop ---
def main():
    # --- Constants ---
    WIDTH, HEIGHT = 1200, 800
    FPS = 60
    BG_COLOR = (30, 30, 30)

    # --- Initialization ---
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Antialiased Drawing with v2/v3")
    clock = pg.time.Clock()

    ctx = Context(screen, (WIDTH, HEIGHT), (0, 0), 5)

    pend = pendulum(0, (0, 0.4), (0, 0), (0, 0))
    pend.setParams()
    pend.run(10, 1 / 60)

    running = True
    i = 0
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(BG_COLOR)

        pend.displayFrame(ctx, pend.h_Q[i], pend.h_dQ[i], pend.h_d2Q[i])

        pg.display.flip()

        i += 1
        i %= len(pend.h_T)

    pg.quit()

if __name__ == "__main__":
    main()