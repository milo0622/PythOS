import os
from pathlib import Path
import sys

args = sys.argv[1:]

def main():
    targetPath = ""
    if not args:
        targetPath = "."
        for item in Path(targetPath).iterdir():
            if item.is_dir():
                print(item + "/", end="    ")
            else:
                print(item, end="    ")
        print("")
    else:
        if len(args) > 1:
            for item in args:
                if Path(item).is_dir() and Path(item).exists():
                    print(f"{item}:")
                    for file in Path(item).iterdir():
                        if file.is_dir():
                            print(f"{file.name}/", end="    ")
                        else:
                            print(f"{file.name}/", end="    ")
                    print("")
                elif Path(item).is_file():
                    print(item)
                elif not Path(item).exists():
                    print(f"ls: cannot access '{item}': No such file or directory")
        else:
            for item in args:
                if Path(item).is_dir() and Path(item).exists():
                    for file in Path(item).iterdir():
                        if file.is_dir():
                            print(f"{file.name}/", end="    ")
                        else:
                            print(f"{file.name}", end="    ")
                    print("")
                elif Path(item).is_file():
                    print(item)
                elif not Path(item).exists():
                    print(f"ls: cannot access '{item}': No such file or directory")

if __name__ == "__main__":
    main()