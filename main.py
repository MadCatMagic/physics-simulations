
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

import imgui.core as imgui
import pygame as pg
import sys

import rendering
from context import Context
import simulation
from vector import v2, v3
from math import pi

SCREENSIZE = (1200, 800)
FPS = 60
BG_COLOUR = (30, 30, 30)

def main():

    # initialisation
    pg.init()
    screen = pg.display.set_mode(SCREENSIZE, pg.DOUBLEBUF | pg.OPENGL)
    pg.display.set_caption("Physics")
    clock = pg.time.Clock()

    # OpenGL/Imgui setup
    imgui.create_context()
    renderer = rendering.Renderer(*SCREENSIZE)

    io = imgui.get_io()
    io.display_size = SCREENSIZE

    # rendering context
    ctx = Context(renderer.pygameSurface, v2(*SCREENSIZE), v2(0, 0), 5)

    # simulation
    pend = simulation.pendulum(0, (0, 0.4), (0, 0), (0, 0))
    pend.setParams()
    pend.run(10, 1 / 60)

    # mainloop
    running = True
    i = 0
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            renderer.impl.process_event(event)
        renderer.impl.process_inputs()

        # do imgui stuff
        imgui.new_frame()
        imgui.begin("Test window")
        imgui.text("heehheee")
        changed = [False for _ in range(7)]
        new_h_Q = [0, 0]
        new_h_dQ = [0, 0]
        changed[0], new_h_Q[0] = imgui.slider_float("x_0", pend.h_Q[0][0], -2.0, 2.0)
        changed[1], new_h_dQ[0] = imgui.slider_float("dx_0", pend.h_dQ[0][0], -1.0, 1.0)
        changed[2], new_h_Q[1] = imgui.slider_float("theta_0", pend.h_Q[0][1], -pi, pi)
        changed[3], new_h_dQ[1] = imgui.slider_float("dtheta_0", pend.h_dQ[0][1], -2 * pi, 2 * pi)
        pend.h_Q[0] = tuple(new_h_Q)
        pend.h_dQ[0] = tuple(new_h_dQ)
        changed[4], pend.m = imgui.slider_float("m", pend.m, 0.0, 10.0)
        changed[5], pend.M = imgui.slider_float("M", pend.M, 0.0, 10.0)
        changed[6], pend.l = imgui.slider_float("l", pend.l, 0.01, 2.0)
        imgui.end()

        if any(changed):
            pend.resetSim()
            pend.run(10, 1 / 60)
            i = 0

        # do pygame stuff
        renderer.pygameSurface.fill(BG_COLOUR)
        pend.displayFrame(ctx, pend.h_Q[i], pend.h_dQ[i], pend.h_d2Q[i])

        renderer.TransferToOpenglTexture()
        renderer.RenderImgui()

        i += 1
        i %= len(pend.h_T)

    renderer.impl.shutdown()
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()