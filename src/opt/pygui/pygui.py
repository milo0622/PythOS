import sys
sys.path.insert(0, "/opt/pygui/")
from lib.initialization import *
from lib.server import *
from lib.uiapi import *
import pygame
from pathlib import Path
import platform

args = sys.argv[1:]

class PyGUI:
    def __init__(self):
        fbPreload()
        initialization = init(pygame, mS=2.5)
        self.screen, self.w, self.h = initialization.initPyGame()
        self.curX, self.curY = initialization.initMouse()

        if len(args) >= 1:
            if args[0] == "debug":
                self.infoPath = "../../etc/os-release"
            else:
                self.infoPath = "/etc/os-release"

    def main(self):
        self.sysServer = SysServer(pygame, self.screen, self.w, self.h)
        self.mainloop()

    def mainloop(self, fps=60):
        clock = pygame.time.Clock()
        running = True

        self.autostart() # <-- Ts is for automatically running programs when pygui starts (obviously)

        while running:
            try:
                mousePos = pygame.mouse.get_pos()
                clock.tick(fps)

                self.sysServer.drawWallpaper()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        print("mouse button down detected")
                        if event.button == 1:
                            for winID in list(self.sysServer.windows.keys())[::-1]:
                                if self.sysServer.windows[winID].handleMouseDown(mousePos):
                                    break
                    elif event.type == pygame.MOUSEBUTTONUP:
                        print("mouse button up detected")
                        if event.button == 1:
                            for winID in list(self.sysServer.windows.keys())[::-1]:
                                if self.sysServer.windows[winID].handleMouseUp(mousePos):
                                    break
                    elif event.type == pygame.MOUSEMOTION:
                        if len(self.sysServer.windows) > 0:
                            topWindow = next(reversed(self.sysServer.windows))
                            topWindow = self.sysServer.windows[topWindow]
                            if topWindow.isDragging:
                                topWindow.moveWindow(event.rel[0], event.rel[1])
                        
                for window in self.sysServer.windows.keys():
                    self.sysServer.windows[window].drawWindow()
            
                self.sysServer.bootFade(0.5)
                pygame.display.flip()
            except (KeyboardInterrupt, EOFError):
                break
    
    def autostart(self):
        _, self.aboutID = self.sysServer.initWindow(w=400, h=400, title="About PythOS", close=True, fontPath="/opt/pygui/assets/defaultFont.ttf")
        self.tempAbout(self.aboutID)
    
    def tempAbout(self, windowID):
        infoContent = f"""
PythOS version: 26.07.1
Codename: Phoenix
Kernel name: {platform.system()}
Kernel release: {platform.release()}
Machine info: {platform.machine()}
OSInfo: {'GNU/Linux' if platform.system() == 'Linux' else platform.system()}
        """
        content = self.sysServer.windows[windowID].content
        title = UIText(targetSurface=content, fontSize=30, fontColor=[0,0,0])
        title.renderText("About PythOS")
        title.blitText(10, 10)
        info = UIText(targetSurface=content, fontSize=15, fontColor=[0,0,0])
        info.renderText(infoContent)
        info.blitText(10, 10 + title.height + 2)
    
if __name__ == "__main__":
    gui = PyGUI().main()
