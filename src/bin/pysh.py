#!/bin/python3

import os
import readline
import subprocess
import sys
from curses import use_default_colors
from pathlib import Path

args = sys.argv[1:]
os.environ["PATH"] = "/usr/bin:/bin:/sbin"


def main():
    user_input = ""
    while True:
        try:
            HOME = os.environ.get("HOME")
            PATH = os.environ.get("PATH").split(":")
            cwd = str(Path.cwd())
            HOME = HOME.rstrip("/")
            if cwd == HOME:
                cwd = "~"
            if cwd.startswith(HOME + "/"):
                cwd = cwd.replace(HOME, "~")
            user_input = input(f"root@PythOS:{cwd}$ ")

            process_user_input(user_input, HOME, PATH)
        except PermissionError:
            print(f"pyshell: {user_input[0]}: Permission denied")
        except KeyboardInterrupt:
            print("")
            continue


def process_user_input(user_input, _HOME, _PATH):
    user_input = user_input.strip().split()
    if not user_input:
        return
    if user_input[0] == "exit":
        sys.exit(1)
    if user_input[0] == "cd":
        if not user_input[1:] or "".join(user_input[1:]).rstrip("/") == "~":
            target_path = _HOME
        else:
            target_path = " ".join(user_input[1:])
        if not Path(target_path).exists():
            print(f"pyshell: {target_path}: No such file or directory")
            return
        os.chdir(target_path)
        return

    target_bin = user_input[0]
    cmd_found = False
    for path in _PATH:
        full_path = os.path.join(path, target_bin)
        if Path(full_path).is_file():
            with open(full_path, "rb") as f:
                start_bytes = f.read(2)
            if start_bytes.startswith(b"#!"):
                shebang_path = ""
                with open(full_path, "r") as file:
                    shebang_path = file.read().splitlines()[0][2:].strip()
                    subprocess.run([shebang_path, full_path] + user_input[1:])
            else:
                subprocess.run([full_path] + user_input[1:])
            cmd_found = True
            break

        py_full_path = full_path + ".py"
        if Path(py_full_path).is_file():
            with open(py_full_path, "rb") as f:
                start_bytes = f.read(2)
            if start_bytes.startswith(b"#!"):
                shebang_path = ""
                with open(py_full_path, "r") as file:
                    shebang_path = file.read().splitlines()[0][2:].strip()
                    subprocess.run([shebang_path, py_full_path] + user_input[1:])
            else:
                subprocess.run(["/bin/python3", py_full_path] + user_input[1:])
            cmd_found = True
            break

        if Path(user_input[0]).is_file():
            with open(user_input[0], "rb") as f:
                startBytes = f.read(2)
                if startBytes == b"#!":
                    with open(user_input[0], "r") as file:
                        shebang_path = file.read().splitlines()[0][2:].strip()
                        subprocess.run([shebang_path, py_full_path] + user_input[1:])
                        cmd_found = True
                        break
                elif user_input[0].endswith(".py"):
                    subprocess.run(["/bin/python3", user_input[0]] + user_input[1:])
                    cmd_found = True
                    break
                else:
                    subprocess.run([user_input[0]] + user_input[1:])
    if not cmd_found:
        print(f"{user_input[0]}: command not found")


if __name__ == "__main__":
    main()
