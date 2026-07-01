import argparse

def main():
    args = parseArgs()
    ignoreNewline = args.n
    ANSIChar = args.e
    text = "".join(args.text)
    if ANSIChar:
        text = bytes(text, "utf-8").decode("unicode_escape")
    echo(text=text, ignoreNewline=ignoreNewline)

def parseArgs():
    parser = argparse.ArgumentParser(description="Print the STRING(s) to standard output.", usage="echo [OPTIONS]... [STRING]...")
    parser.add_argument("-n", help="Do not print the trailing newline character.", action="store_true")
    parser.add_argument("-e", help="Allows printing ANSI or backslash code.", action="store_true")
    parser.add_argument("text", help="Text to be printed", nargs="*")
    return parser.parse_args()

def echo(text="", ignoreNewline=False):
    print(text, end="" if ignoreNewline else "\n")

if __name__ == "__main__":
    main()