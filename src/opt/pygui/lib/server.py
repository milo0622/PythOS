import sys
sys.path.insert("/opt/pygui")
from lib.windowapi import *

class SysServer:
    def __init__(self, pygame, targetSurface, w=800, h=600):
        self.pygame = pygame
        self.tS = targetSurface
        self.w = w
        self.h = h
	
	self.windows = []

    def drawWallpaper(self, color:list=[0, 128, 128]):
        self.tS.fill(color)    
    
    def initWindow(self, targetSurface, w=400, h=300, title="window", x=0, y=0, close=True):
    	window = WindowAPI(targetSurface, x, y, width, height, title, close)
	self.windows.append(window)
