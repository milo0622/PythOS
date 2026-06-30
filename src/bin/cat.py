import argparse
import os
from pathlib import Path

def main():
    args = parseArgs()
    displayFile(files=args.files, nonblank=args.number_nonblank, showEnds=args.show_ends, number=args.number, showTabs=args.show_tabs, ignore=args.ignore_errors)
def parseArgs():
    parser = argparse.ArgumentParser(
        description="""Concatenate FILE(s), or standard input, to standard output
With no FILE, or when FILE is -, read standard input.""", 
        usage="cat [OPTION]... [FILE]..."
    )
    parser.add_argument("-b", "--number-nonblank", help="number nonempty output lines, overrides -n", action="store_true")
    parser.add_argument("-E", "--show-ends", help="display $ at end of each line", action="store_true")
    parser.add_argument("-n", "--number", help="number all output lines", action="store_true")
    parser.add_argument("-T", "--show-tabs", help="display TAB characters at ^I", action="store_true")
    parser.add_argument("-i", "--ignore-errors", help="ignore errors occurred during file display", action="store_true")
    parser.add_argument("files", nargs="*", help="input files to be displayed")

    return parser.parse_args()

def displayFile(files=[], nonblank=False, showEnds=False, number=False, showTabs=False, ignore=False):
    content = ""
    if not files:
        noFiles()
        return
    for file in files:
        finalResult = []
        try:
            if Path(file).is_file():
                with open(file, "r") as f:
                    content = f.read()
                    rawLines = content.splitlines()
                    finalResult = rawLines.copy()
                if nonblank and number:
                    number = False
                if showEnds:
                    for idx, line in enumerate(finalResult):
                        finalResult[idx] = f"{line}$"
                if showTabs:
                    for idx, line in enumerate(finalResult):
                        finalResult[idx] = line.replace("\t", "^I")
                if nonblank:
                    blanks = 0
                    for idx, line in enumerate(finalResult):
                        if not rawLines[idx]:
                            finalResult[idx] = ""
                            blanks += 1
                            continue
                        finalResult[idx] = f"    {idx - blanks + 1}  {line}"
                if number:
                    for idx, line in enumerate(finalResult):
                        finalResult[idx] = f"    {idx + 1}  {line}"

                print("\n".join(finalResult))
            elif Path(file).is_dir():
                print(f"cat: '{file}' is a directory")
                continue
            else:
                print(f"cat: '{file}': No such file or directory")

        except Exception as e:
            if ignore:
                continue
            else:
                print(f"cat: Error reading '{file}': {e}")
                return
    
def noFiles():
    print("cat: No input files")
    return
if __name__ == "__main__":
    main()