

import imgui.core as imgui
import pygame as pg
import sys

import rendering
from context import Context
import simulation
from vector import v2, v3
from math import pi

SCREENSIZE = (800, 600)
FPS = 60
BG_COLOUR = (30, 30, 30)

def simulate(sim: simulation.Sim, caption: str = "Physics", worldCentre: v2 = v2(0, 0), worldDiameter: float = 5, timestep: float = 1 / 60, itersPerTimestep: int = 1):

    # initialisation
    pg.init()
    screen = pg.display.set_mode(SCREENSIZE, pg.DOUBLEBUF | pg.OPENGL)
    pg.display.set_caption(caption)
    clock = pg.time.Clock()

    # OpenGL/Imgui setup
    imgui.create_context()
    renderer = rendering.Renderer(*SCREENSIZE)

    io = imgui.get_io()
    io.display_size = SCREENSIZE

    # rendering context
    ctx = Context(renderer.pygameSurface, v2(*SCREENSIZE), worldCentre, worldDiameter)

    # simulation
    #pend = simulation.pendulum2(0, (0.2, 0.4), (0, 0), (0, 0))
    sim.setParams()

    # mainloop
    running = True
    i = 0
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            renderer.impl.process_event(event)
            if renderer.impl.io.want_capture_mouse or renderer.impl.io.want_capture_keyboard:
                continue
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                sim.onClick(ctx.inverseTransform(pos), {1: 0, 3: 1}[event.button])
        
        renderer.impl.process_inputs()

        # do imgui stuff
        imgui.new_frame()
        imgui.begin("Test window")
        changedSize, newSize = imgui.slider_float("display scale", ctx.size, 1, 10)
        if changedSize:
            ctx.setSize(newSize)
        imgui.text("settings")
        changed = sim.guiEditables()
        imgui.end()

        if changed:
            sim.resetSim()
            #pend.run(20, 1 / 120)
            i = 0

        # do pygame stuff
        renderer.pygameSurface.fill(BG_COLOUR)
        for iter in range(itersPerTimestep):
            sim.update(timestep / itersPerTimestep, iter == itersPerTimestep - 1)
        sim.displayFrame(ctx, sim.h_Q[i], sim.h_dQ[i], sim.h_d2Q[i])

        renderer.TransferToOpenglTexture()
        renderer.RenderImgui()

        i += 1
        #i += 2
        #i %= len(pend.h_T)

    renderer.impl.shutdown()
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    simulate(simulation.pendulum(float, 0, (0, 0.4), (0, 0)))