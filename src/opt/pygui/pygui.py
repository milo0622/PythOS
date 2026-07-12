import sys
sys.path.insert(0, "/opt/pygui/")
from lib.initialization import *
from lib.server import *
from lib.windowapi import *
import pygame

def main():
    fbPreload()
    initialization = init(pygame, mS=2.5)
    screen, w, h = initialization.initPyGame()
    curX, curY = initialization.initMouse()

    sysServer = SysServer(pygame, screen, w, h)
    mainloop(sysServer)

def mainloop(sysServer, fps=60):
    clock = pygame.time.Clock()
    running = True
    testing = WindowAPI(screen, x=0, y=0, width=400, height=300, title="Testing", close=True)

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        sysServer.drawWallpaper()

        testing.drawWindow()
	
        pygame.display.flip()

if __name__ == "__main__":
    main()
