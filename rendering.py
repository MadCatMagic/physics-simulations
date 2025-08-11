import OpenGL.GL as gl
import pygame as pg
import imgui.core as imgui
from imgui.integrations.pygame import PygameRenderer

class Renderer:
    def __init__(self, w, h):
        self.textureID = gl.glGenTextures(1)

        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-1, 1, -1, 1, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glClearColor(0.1, 0.1, 0.1, 1)

        self.pygameSurface = pg.Surface((w, h))
        self.impl = PygameRenderer()

    def SurfaceToTexture(self, surface):
        """Uploads a pygame surface to an OpenGL texture."""
        surf_data = pg.image.tostring(surface, "RGBA", False)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, surface.get_width(),
                    surface.get_height(), 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, surf_data)

    def DrawTextureFullscreen(self):
        """Draw the texture as a fullscreen quad."""
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureID)
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(0, 0); gl.glVertex2f(-1, 1)
        gl.glTexCoord2f(1, 0); gl.glVertex2f(1, 1)
        gl.glTexCoord2f(1, 1); gl.glVertex2f(1, -1)
        gl.glTexCoord2f(0, 1); gl.glVertex2f(-1, -1)
        gl.glEnd()
        gl.glDisable(gl.GL_TEXTURE_2D)

    def TransferToOpenglTexture(self):
        # transfer to texture
        self.SurfaceToTexture(self.pygameSurface)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.DrawTextureFullscreen()

    def RenderImgui(self):
        # render imgui stuff
        imgui.render()
        self.impl.render(imgui.get_draw_data())
        pg.display.flip()