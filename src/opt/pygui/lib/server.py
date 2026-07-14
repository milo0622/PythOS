import sys
sys.path.insert(0, "/opt/pygui")
from lib.uiapi import *

class SysServer:
    def __init__(self, pygame, targetSurface, screenw=800, screenh=600):
        self.pygame = pygame
        self.tS = targetSurface
        self.w = screenw
        self.h = screenh

        self.windows = {}
        self.nextID = 0

    def drawWallpaper(self, color:list=[0, 128, 128]):
        self.tS.fill(color)    

    def initWindow(self, w=400, h=300, title="window", x=None, y=None, close=True, fontPath=None):
        if not x and not y:
            if self.w is None and self.h is None:
                x, y = 0,0
            else:
                x, y = ((self.w - w) // 2), ((self.h - h) // 2)

        window = WindowAPI(sysServer=self, targetSurface=self.tS, x=x, y=y, width=w, height=h, title=title, close=close, fontPath=fontPath)
        self.windows[self.nextID] = window
        currentID = self.nextID
        window.ID = currentID
        
        self.nextID += 1

        return window, currentID
