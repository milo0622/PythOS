import pygame

class WindowAPI:
    def __init__(self, targetSurface:pygame.Surface, width=400, height=300, title="window"):
        self.w = width
        self.h = height
        self.title = title

    def drawWindow(self):
        pass
