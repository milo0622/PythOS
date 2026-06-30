import readline
import sys
import argparse
from pathlib import Path
import os
import subprocess

DEFAULTMSG = "Welcome to PythOS!"

def welcomeMessage(msgPath:str="/etc/motd"):
    if Path(msgPath).exists() and Path(msgPath).is_file():
        try:
            with open(msgPath, "r") as msgObj:
                lines = msgObj.read().splitlines()
            for line in lines:
                print(line)
        except Exception as e:
            print(f"MOTD cannot be read: {e}")
    else:
        try:
            Path(os.path.dirname(msgPath)).mkdir(parents=True, exist_ok=True)
            Path(msgPath).touch()
            with open(msgPath, "w") as f:
                f.write(DEFAULTMSG)
            for line in DEFAULTMSG.splitlines():
                print(line)
        except PermissionError:
            print("Permission denied.")
def main():
    print("\033[H\033[2J")
    HOME = os.getenv("HOME")
    PATH = os.getenv("PATH")
    if not isinstance(PATH, str):
        PATH = "/bin:/sbin:/usr/bin".split(":")
    else:
        PATH = PATH.split(":")
    if not Path(HOME).exists():
        Path(HOME).mkdir(parents=True, exist_ok=True)
    HOME = standardizeHome(HOME)
    welcomeMessage()
    while True:
        try:
            uInput = input(f"root@PythOS:{decodePath(path=os.getcwd(), HOME=HOME)}$ ")
        except (EOFError, KeyboardInterrupt):
            print()
            continue
        if not uInput.strip():
            continue

        uInput = uInput.split()
        cmd = uInput[0]
        if cmd == "exit":
            print("logout")
            sys.exit(1)
        if cmd == "cd":
            if len(uInput) > 2:
                print("cd: Too many arguments")
                continue
            if len(uInput) == 1:
                chdir("", HOME=HOME)
            else:
                chdir(path=uInput[1], HOME=HOME)
            continue
        successful = False
        if Path(cmd).is_file():
            successful = True
            exec(cmd, uInput[1:])
            continue
        if Path(f"{cmd}.py").is_file():
            successful = True
            exec(f"{cmd}.py", uInput[1:])
            continue
        for item in PATH:
            if len(cmd.split("/")) == 1 or len(cmd.split("/")) == 2 and cmd.split("/")[0] == ".":
                if Path(f"{item}/{cmd}").is_file():
                    successful = True
                    exec(f"{item}/{cmd}", uInput[1:])
                    break
                elif Path(f"{item}/{cmd}.py").is_file():
                    successful = True
                    exec(f"{item}/{cmd}.py", uInput[1:])
                    break
                else:
                    continue
        if not successful:
            print(f"pysh: {cmd}: No such file or directory")

def decodePath(path:str=os.getcwd(), HOME:str="/root") -> str:
    if Path(path).is_relative_to(HOME):
        return path.replace(HOME, "~")
    return path
    
def standardizeHome(HOME:str="/root"):
    if HOME.endswith("/"):
        HOME = HOME[:-1]
    return HOME

def chdir(path:str="", HOME:str="/root"):
    path = (path.strip())
    if not path or path == "~":
        try:
            os.chdir(HOME)
            return
        except Exception as e:
            return
    path = encodePath(path)
    if not Path(path).exists():
        print(f"cd: {path}: No such file or directory")
        return
    if not Path(path).is_dir():
        print(f"cd: not a directory: {path}")
        return
    try:
        os.chdir(path)
    except PermissionError:
        print(f"cd: {path}: Permission denied")
    except Exception as e:
        print(f"cd: {path}: {e}")

def encodePath(path:str="", HOME:str="/root"):
    if path.startswith("~"):
        return path.replace("~", HOME)
    return path

def exec(binPath:str, args:list):
    try:
        if binPath.endswith(".py"):
            args.insert(0, binPath)
            if Path("/usr/bin/python3").is_file():
                args.insert(0, "/usr/bin/python3")
            else:
                args.insert(0, "/opt/homebrew/bin/python3") # Debug for my mac
            subprocess.run(args=args, check=True, shell=False)
            return
        else:
            args.insert(0, binPath)
            subprocess.run(args=args, check=True, shell=False)
            return
    except subprocess.CalledProcessError:
        return
    except PermissionError:
        print(f"pysh: {binPath}: Permission denied")
        return
    except Exception as e:
        print(f"Error executing: {binPath}: {e}")
        return

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
