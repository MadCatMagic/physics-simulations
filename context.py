from vector import v2

import pygame as pg
import pygame.gfxdraw as gfxdraw

class Context:
    def __init__(self, screen: pg.Surface, screenSize: v2, centre: v2, size: float):
        self.screen = screen
        self.centre = v2(centre.x - size * 0.5, centre.y - size * screenSize.y / screenSize.x * 0.5)
        self.size = size
        self.screenSize = screenSize

        self.col: tuple[int, int, int] = (255, 255, 255)

    def transform(self, p: v2) -> tuple[int, int]:
        return (
            int((p.x - self.centre.x) / self.size * self.screenSize.x), 
            int(self.screenSize.y - (p.y - self.centre.y) / self.size * self.screenSize.x)
        )

    def line(self, p1: v2, p2: v2):
        gfxdraw.line(self.screen, *self.transform(p1), *self.transform(p2), self.col)

    def rect(self, centre: v2, size: v2):
        c = self.transform(v2(centre.x - size.x, centre.y + size.y))
        hs = (
            int(size.x / self.size * self.screenSize.x), 
            int(size.y / self.size * self.screenSize.x)
        )
        #pg.gfxdraw.aacircle(self.screen, c[0], c[1], , color.to_color_tuple())
        #pg.gfxdraw.filled_circle(self.screen, int(center.x), int(center.y), radius, color.to_color_tuple())

        pg.draw.rect(self.screen, self.col, (c[0], c[1], hs[0] * 2, hs[1] * 2), 0)

    def circle(self, centre: v2, radius: float):
        c = self.transform(centre)
        r = int(radius / self.size * self.screenSize.x)
        gfxdraw.aacircle(self.screen, c[0], c[1], r, self.col)
        gfxdraw.filled_circle(self.screen, c[0], c[1], r, self.col)