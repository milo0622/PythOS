class SysServer:
    def __init__(self, pygame, targetSurface, w=800, h=600):
        self.pygame = pygame
        self.tS = targetSurface
        self.w = w
        self.h = h

    def drawWallpaper(self, color:list=[0, 128, 128]):
        self.tS.fill(color)    
    
