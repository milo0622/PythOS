import argparse
import sys
import os
from pathlib import Path
import shutil

def main():
    parsed = parseArgs()
    recursive = parsed.recursive
    verbose = parsed.verbose
    source = parsed.paths[:-1]
    dest = str(parsed.paths[-1])
    if verification(destPath=dest, sources=source):
        copyFiles(recursive=recursive, verbose=verbose, source=source, destPath=dest)
    else:
        return

def parseArgs():
    parser = argparse.ArgumentParser(
        description="copy files",
        usage="cp [OPTION]... SOURCE... DEST"
    )
    parser.add_argument("-r", "--recursive", help="Recursive mode. Copies directories and all of their contents", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose mode. Shows what are being copied", action="store_true")
    parser.add_argument("paths", nargs="+", help="Source paths followed by destination")

    return parser.parse_args()

def copyFiles(recursive=False, verbose=False, source="", destPath=""):
    dest = Path(destPath)

    for item in source:
        if dest.is_dir():
            targetDest = dest /     Path(item).name
        else:
            targetDest = dest
        try:
            if Path(item).is_dir():
                if not recursive:
                    print(f"cp: {item}: Is a directory (not copied)")
                    continue
                shutil.copytree(item, targetDest, dirs_exist_ok=True)
                if verbose:
                    print(f"{item} -> {targetDest}")
                continue
            if Path(item).is_file():
                shutil.copy2(item, targetDest)
            if verbose:
                print(f"{item} -> {targetDest}")
            continue
        except PermissionError:
            print("cp: Permission denied")
            continue
        except Exception as e:
            print(f"cp: {e}")
                

def verification(destPath="", sources=[]) -> bool:
    parent = Path(os.path.dirname(destPath) or ".")
    dest = Path(destPath)
    if dest.exists():
        if dest.is_dir():
            return True
        else:
            if len(sources) > 1:
                print(f"cp: target '{destPath}' is not a directory")
                return False
            return True
    else:
        if len(sources) > 1:
            print(f"cp: target '{destPath}' is not a directory")
            return False
        if not parent.exists():
            print(f"cp: cannnot create regular file '{destPath}': No such file or directory")
            return False
        if not parent.is_dir():
            print(f"cp: '{destPath}': No such file or directory")
            return False
    return True

if __name__ == "__main__":
    main()