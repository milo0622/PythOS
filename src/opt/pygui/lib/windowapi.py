import pygame

class WindowAPI:
    def __init__(self, targetSurface:pygame.Surface, x=0, y=0, width=400, height=300, title="window", close=True):
        self.w = width
        self.h = height
	self.x = x
	self.y = y

        self.title = title
	self.targetSurface = targetSurface

	self.bgColor = [212, 208, 200]
	self.lightMargin = [255, 255, 255]
	self.darkMargin = [0,0,0]

	self.tbColor = [0,0,128]
	self.tbWidth = width - 6
	self.tbHeight = 25
	
	self.close = close

	self.xOffset = 0
	self.yOffset = 0
	
	self.window = None
	self.titleBar = None

    def drawWindow(self):
        self.window = pygame.Surface((self.w, self.h))
	self.window.fill(self.bgColor)

	pygame.draw.line(self.window, self.lightMargin, (0, 0), (self.w, 0), width=2)
	pygame.draw.line(self.window, self.lightMargin, (0,0), (0, self.h), width=2)
	pygame.draw.line(self.window, self.darkMargin, (self.w - 1, 0), (self.w - 1, self.h - 1), width=2)
	pygame.draw.line(self.window, self.darkMargin, (0, self.h - 1), (self.w - 1, self.h - 1), width=2)
	
	self.titleBar = pygame.draw.rect(self.window, self.tbColor, (2, 2, self.tbWidth, self.tbHeight))
	self.content = pygame.Surface((self.w - 6, self.h - 4 - self.tbHeight))
	self.window.blit(self.content, (2, self.tbHeight + 4))
	
        self.targetSurface.blit(self.window, (self.x, self.y))
	return self.window, self.titleBar, self.content
