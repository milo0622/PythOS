import sys
sys.path.insert(0, "/opt/pygui/")
from lib.initialization import *
from lib.server import *
from lib.uiapi import *
import pygame

class PyGUI:
    def __init__(self):
        fbPreload()
        initialization = init(pygame, mS=2.5)
        self.screen, self.w, self.h = initialization.initPyGame()
        self.curX, self.curY = initialization.initMouse()

    def main(self):
        self.sysServer = SysServer(pygame, self.screen, self.w, self.h)
        self.mainloop()

    def mainloop(self, fps=60):
        clock = pygame.time.Clock()
        running = True
        window, ID = self.sysServer.initWindow(w=400, h=300, title="About PythOS", close=True, fontPath=None)

        while running:
            try:
                clock.tick(fps)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                
                self.sysServer.drawWallpaper()

                for window in self.sysServer.windows.keys():
                    self.sysServer.windows[window].drawWindow()
            
                pygame.display.flip()
            except (KeyboardInterrupt, EOFError):
                print("\033[?25h")
                break

if __name__ == "__main__":
    gui = PyGUI().main()
