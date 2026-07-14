import pygame
from pathlib import Path
import sys
sys.path.insert(0,"/opt/pygui")
from lib.server import *

class WindowAPI:
	def __init__(self, sysServer:SysServer, targetSurface:pygame.Surface, x, y, width=400, height=300, title="window", close=True, fontPath=None):
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
		self.tbStartX = 2
		self.tbStartY = 2

		self.close = close

		self.xOffset = 0
		self.yOffset = 0

		self.window = None
		self.titleBar = None

		self.titleFS = 20
		self.font = pygame.font.Font(fontPath, size=self.titleFS)

		self.ID = None

		closeBtnWH = self.tbHeight - 6
		closeBtnY = (self.tbHeight - closeBtnWH) // 2 + self.tbStartY
		closeBtnX = (self.w - self.tbStartX - closeBtnWH - closeBtnY)
		self.closeBtn = UIButton(closeBtnWH, closeBtnWH, closeBtnX, closeBtnY, callback=self.closeWindow, renderText=("x", 24))

	def drawWindow(self):
		self.window = pygame.Surface((self.w, self.h))
		self.window.fill(self.bgColor)

		drawShadowsonSurface(self.window, self.w, self.h)

		self.titleBar = pygame.Rect(2, 2, self.tbWidth, self.tbHeight)
		pygame.draw.rect(self.window, self.tbColor, self.titleBar)
		self.titleObject = self.font.render(self.title, True, [255, 255, 255])

		titleY = (self.tbHeight - int(self.font.get_height())) // 2 + self.tbStartY
		self.window.blit(self.titleObject, (titleY, titleY))

		if self.close:
			self.closeBtn.drawAsRect(self.window)

		self.content = pygame.Surface((self.w - 6, self.h - 6 - self.tbHeight))
		self.content.fill(self.bgColor)
		self.window.blit(self.content, (2, self.tbHeight + 4))

		self.targetSurface.blit(self.window, (self.x, self.y))
		return self.window, self.titleBar, self.titleObject, self.content
	
	def closeWindow(self):
		self.sysServer.windows.pop(self.ID)

def drawShadowsonSurface(targetSurface, surfacew, surfaceh, lightMargin=[255, 255, 255], darkMargin=[0,0,0], grayMargin=[100, 100, 100], width=2):
	topleft = (0, 0)
	topright = (surfacew - width, 0)
	bottomleft = (0, surfaceh - width)
	bottomright = (surfacew - width, surfaceh - width)
	pygame.draw.line(targetSurface, lightMargin, topleft, bottomleft, width=width )
	pygame.draw.line(targetSurface, lightMargin, topleft, topright, width=width)
	pygame.draw.line(targetSurface, darkMargin, topright, (bottomright[0], bottomright[1] + width // 2), width=width)
	pygame.draw.line(targetSurface, darkMargin, bottomleft, (bottomright[0] + width // 2, bottomright[1]), width=width)

def drawShadowsonRect(parentSurface, targetRect:pygame.Rect, lightMargin=[255, 255, 255], darkMargin=[0,0,0], grayMargin=[80,80,80]):
	topleft = targetRect.topleft
	topright = targetRect.topright
	bottomleft = targetRect.bottomleft
	bottomright = targetRect.bottomright
	rectw = targetRect.width
	recth = targetRect.height
	pygame.draw.line(parentSurface, lightMargin, topleft, bottomleft)
	pygame.draw.line(parentSurface, lightMargin, topleft, topright)
	pygame.draw.line(parentSurface, darkMargin, topright, bottomright)
	pygame.draw.line(parentSurface, darkMargin, bottomleft, bottomright)
	pygame.draw.line(parentSurface, grayMargin, (topright[0] - 1, topright[1] + 1), (bottomright[0] - 1, bottomright[1]))
	pygame.draw.line(parentSurface, grayMargin, (bottomleft[0] + 1, bottomleft[1] - 1), (bottomright[0] - 1, bottomright[1] - 1))

class UIButton:
	def __init__(self, w, h, x, y, callback, renderText=("", 24), renderImagePath="", color:pygame.Color=[212, 208, 200]):
		self.w = w
		self.h = h
		self.x = x
		self.y = y

		self.callback = callback
		self.isClicked = False

		self.font = pygame.font.Font(None, renderText[1])
		self.text = renderText[0]

		self.color = color

		if not renderImagePath:
			self.imageObject = None
		elif Path(renderImagePath).exists():
			self.imageObject = pygame.image.load(renderImagePath)

	def draw(self, tS:pygame.Surface):
		self.tS = tS
		self.buttonObject = pygame.Surface((self.w, self.h))
		self.buttonObject.fill(self.color)
		drawShadowsonSurface(self.buttonObject, self.w, self.h)

		if self.text is not None:
			self.textObject = self.font.render(self.text, True, [0,0,0])
		
		if self.imageObject is not None:
			imageX = (self.w - self.imageObject.get_width()) // 2
			imageY = (self.h - int(self.imageObject.get_linesize())) // 2
			self.buttonObject.blit(self.imageObject, [imageX, imageY])

		if self.textObject:
			textX = (self.w - self.textObject.get_width()) // 2
			textY = (self.h - int(self.textObject.get_height())) // 2
			self.buttonObject.blit(self.textObject, [textX, textY])
		
		self.tS.blit(self.buttonObject, (self.x, self.y))
		return self.buttonObject, self.imageObject, self.textObject
	
	def drawAsRect(self, tS:pygame.Surface):
		self.tS = tS
		self.buttonObject = pygame.Rect((self.x, self.y, self.w, self.h))
		pygame.draw.rect(self.tS, self.color, self.buttonObject)

		if self.text is not None:
			self.textObject = self.font.render(self.text, True, [0,0,0])
		if self.imageObject is not None:
			imageX = (self.w - self.imageObject.get_width()) // 2 + self.x
			imageY = (self.h - int(self.imageObject.get_linesize())) // 2 + self.y
			self.tS.blit(self.imageObject, (imageX, imageY))
		if self.textObject is not None:
			textX = (self.w - self.textObject.get_width()) // 2 + self.x
			textY = (self.h - self.textObject.get_height()) // 2 + self.y
			self.tS.blit(self.textObject, (textX, textY))

		drawShadowsonRect(tS, self.buttonObject)

		return self.buttonObject, self.imageObject, self.textObject
