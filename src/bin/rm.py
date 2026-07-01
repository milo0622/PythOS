import argparse
import os
import shutil
from pathlib import Path

def main():
    parser = parseArgs()
    args = parser.parse_args()
    recursive = args.recursive
    force = args.force
    verbose = args.verbose
    confirmation = args.i
    files = args.files
    if not files:
        parser.print_help()
        return
    removeFiles(recursive=recursive, force=force, verbose=verbose, confirmation=confirmation, files=files)

def parseArgs():
    parser = argparse.ArgumentParser(
        description="Delete files or directories", 
        usage="rm [OPTION]... [FILE]..."
    )
    parser.add_argument("-r", "--recursive", help="Recursive. Allows the deletion of folders.", action="store_true")
    parser.add_argument("-f", "--force", help="Forces the deletion of each file and suppresses errors.", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose. Be verbose when deleting files.", action="store_true")
    parser.add_argument("-i", help="Confirmation before deleting each file.", action="store_true")
    parser.add_argument("files", nargs="*", help="Files to be deleted")

    return parser

def removeFiles(recursive=False, force=False, verbose=False, confirmation=False, files=[]):
    for file in files:
        if not Path(file).exists() and not Path(file).is_symlink():
            if not force: print(f"rm: {file}: No such file or directory")
            continue
        if Path(file).is_dir():
            if not recursive:
                print(f"rm: {file}: Is a directory (Not deleted)")
                continue
            if confirmation:
                confirm = input(f"examine files in directory {file}?")
                if confirm.lower().strip() == "y":
                    for f in Path(file).iterdir():
                        print(f.name)
                confirm = input(f"remove {file}?")
                if confirm.lower().strip() == "y":
                    try:
                        shutil.rmtree(file)
                        if verbose: print(file)
                    except Exception as e:
                        if not force: print(f"rm: {e}")
                continue
            try:
                shutil.rmtree(file)
                if verbose: print(file)
            except Exception as e:
                if not force: print(f"rm: {e}")
            continue
        if confirmation:
            confirm = input(f"remove {file}?")
            if confirm.lower().strip() == "y":
                try:
                    Path(file).unlink()
                    if verbose: print(file)
                except Exception as e:
                    if not force: print(f"rm: {e}")
            continue
        try:
            Path(file).unlink()
            if verbose: print(file)
        except Exception as e:
            if not force: print(f"rm: {e}")
        continue

if __name__ == "__main__":
    main()