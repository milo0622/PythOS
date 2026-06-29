import curses
import subprocess
import os
import time
import sys

args = sys.argv[1:]
debug = False
if len(args) >= 1:
    if args[0] == "dev":
        debug = True
shellPath = "bin/pysh.py" if debug else "/bin/pysh.py"
pythonPath = "/opt/homebrew/bin/python3" if debug else "/bin/python3"

def main():
    showInitMessage()
    try:
        proc = subprocess.run([pythonPath, shellPath], check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            pass
        elif e.returncode != 0: 
            print(f"Failed to initialize PyShell, error: {e}")
        while True:
            try:
                action = curses.wrapper(logonMenu)
                if action == "LOGON":
                    subprocess.run([pythonPath, shellPath])
            except KeyboardInterrupt:
                continue

def showInitMessage(path="/etc/pysh_wmsg"):
    try:
        with open(path, "r") as f:
            welcomeMsg = f.read().splitlines()
            f.close()
        for line in welcomeMsg:
            if line.strip().startswith("#"):
                continue
            print(line)
    except FileNotFoundError:
        return
def drawMenu(stdscr, menu, selected, title, additionalTitle=""):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    titleMsg = ((w - len(title)) // 2 - 1) * " " + title + ((w - len(title)) // 2) * " "
    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr(0, 0, titleMsg)
    stdscr.attroff(curses.A_REVERSE)
    largestItem = max(menu, key=len)
    for idx, item in enumerate(menu):
        padding = ((len(largestItem) - len(item)) // 2) * " " + "  "
        item = padding + item + padding
        x = (w - len(item)) // 2
        y = 3 + idx

        if idx == selected:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, item)
    if additionalTitle:
        stdscr.addstr(4 + len(menu), (w - len(additionalTitle)) // 2, additionalTitle)
    stdscr.refresh()

def logonMenu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.cbreak()
    stdscr.keypad(True)

    menu = [
        "LOGON", 
        "REBOOT", 
        "POWER OFF",
        "HALT SYSTEM"
    ]

    if debug:
        menu.append("EXIT")

    title = "PythOS LOGON MENU"
    selected = 0 

    drawMenu(stdscr=stdscr, title=title, menu=menu, selected=selected)
    additionalTitle = ""
    execution = []
    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected = len(menu) - 1 if selected == 0 else selected - 1
        elif key == curses.KEY_DOWN:
            selected = 0 if selected == len(menu) - 1 else selected + 1
        elif key in (curses.KEY_ENTER, 10, 13):
            if menu[selected] == "LOGON":
                stdscr.clear()
                curses.curs_set(1)
                curses.endwin()
                return "LOGON"
            elif menu[selected] == "POWER OFF":
                additionalTitle = "The system will shutdown NOW!"
                execution = ["/sbin/shutdown"]
            elif menu[selected] == "REBOOT":
                additionalTitle = "The system will reboot NOW!"
                execution = ["/sbin/reboot"]
            elif menu[selected] == "HALT SYSTEM":
                additionalTitle = "The system will halt NOW!"
                execution = ["/sbin/halt"]
            elif menu[selected] == "EXIT":
                sys.exit()
        drawMenu(stdscr=stdscr, menu=menu, selected=selected, title="PythOS LOGON MENU", additionalTitle=additionalTitle)
        if len(execution) > 0:
            if execution[0].startswith("/sbin/"):
                import time
                time.sleep(2)

                subprocess.run(execution)
                continue
            try:
                subprocess.run(execution, check=True)
            except subprocess.CalledProcessError as e:
                continue

if __name__ == "__main__":
    main()