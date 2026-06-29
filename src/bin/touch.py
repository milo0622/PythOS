from pathlib import Path
import os
import argparse
import time

def main():
    parsed = parseArgs()
    createFile(create=parsed.no_create, files=parsed.files, access=parsed.a, mod=parsed.m, ignore=parsed.ignore_errors)

def parseArgs():
    parser = argparse.ArgumentParser(
        description="Update the access and modification times of each FILE to the current time.", 
        usage="touch [OPTION]... [FILE]..."
    )
    parser.add_argument("-a", help="change only the access time", action="store_true")
    parser.add_argument("-m", help="change only the modification time", action="store_true")
    parser.add_argument("-c", "--no-create", help="do not create any files", action="store_false")
    parser.add_argument("-i", "--ignore-errors", help="ignore errors during file modification/creation", action="store_true")
    parser.add_argument("files", nargs="*", help="files to modify")

    return parser.parse_args()

def createFile(create=True, files=[], access=False, mod=False, ignore=False):
    currentTime = time.time()
    if not files:
        noInput()
        return
    for file in files:
        try:
            if create:
                if not Path(file).exists():
                    Path(file).touch()
                    continue
                if access or mod:
                    fileMD = os.stat(file)
                    if access:
                        fileMTime = fileMD.st_mtime
                        os.utime(file, (currentTime, fileMTime))
                    if mod:
                        fileATime = fileMD.st_atime
                        os.utime(file, (fileATime, currentTime))
                    continue
                if not access and not mod:
                    Path(file).touch()
                    continue
            else:
                fileMD = os.stat(file)
                fileATime = fileMD.st_atime
                fileMTime = fileMD.st_mtime
                if not access and not mod:
                    Path(file).touch()
                    continue
                if access:
                    os.utime(file, (currentTime, fileMTime))
                if mod:
                    os.utime(file, (fileATime, currentTime))
        except Exception as e:
            if ignore:
                continue
            print(f"touch: Error setting times of '{file}': {e}")

def noInput():
    print("touch: missing file operand\nTry 'touch --help' for more information.")
    return

if __name__ == "__main__":
    main()
    