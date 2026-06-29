import argparse
from pathlib import Path
import os

def main():
    parsed = defineArgs()
    if not parsed.directories:
        noArgs()
        return
    octal_mode = None
    if parsed.mode:
        try: 
            octal_mode = int(parsed.mode, 8)
        except:
            print("mkdir: Invalid permission mode")
            return
    targets = parsed.directories
    parents = parsed.parents
    for target in targets:
        if Path(target).exists() and not parents:
            print(f"mkdir: {target}: File exists")
            continue
        if not Path(os.path.dirname(target)).exists() and not parents:
            print(f"mkdir: {target}: No such file or directory")
            continue
        Path(target).mkdir(parents=parents, exist_ok=True)
        if parsed.mode is not None and octal_mode is not None:
            os.chmod(target, octal_mode)
        continue
    
def defineArgs():
    parser = argparse.ArgumentParser(
        description="Create the given DIRECTORY(ies) if they do not exist",
        usage="mkdir [OPTION]... DIRECTORY..."
    )

    parser.add_argument("-m", "--mode", type=str, help="set file mode")
    parser.add_argument("-p", "--parents", action="store_true", help="make parent directories as needed")

    parser.add_argument("directories", nargs="*", help="directories to create")
    return parser.parse_args()

def noArgs():
    print("""\x1b[31merror\033[0m: the following required arguments were not provided:
  <dirs>...

Usage: mkdir [OPTION]... DIRECTORY...

For more information, try '--help'.""")

if __name__ == "__main__":
    main()
