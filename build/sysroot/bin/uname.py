import platform
import argparse
import sys

ending="\n"

def main():
    parsed = parseArgs()
    if parsed.all:
        global ending
        ending = " "
        kernelName()
        kernelRel()
        machineInfo()
        OSInfo()
        return
    if parsed.kernel_name:
        kernelName()
    if parsed.kernel_release:
        kernelRel()
    if parsed.machine:
        machineInfo()
    if parsed.operating_system:
        OSInfo()
    if len(sys.argv) == 1:
        kernelName()
    return

def parseArgs():
    parser = argparse.ArgumentParser(
        description="Print certain system information",
        usage="uname [OPTION]"
    )

    parser.add_argument("-a", "--all", action="store_true", help="Behave as though all of the options -mnrsvo were specified.")
    parser.add_argument("-s", "--kernel-name", action="store_true", help="print the kernel name")
    parser.add_argument("-r", "--kernel-release", action="store_true", help="print the operating system release")
    parser.add_argument("-m", "--machine", action="store_true", help="print the machine hardware name")
    parser.add_argument("-o", "--operating-system", action="store_true", help="print the operating system name")

    return parser.parse_args()

def kernelName():
    print(platform.system(), end=ending)

def kernelRel():
    print(platform.release(), end=ending)

def machineInfo():
    print(platform.machine(), end=ending)

def OSInfo():
    if platform.system() == "Linux":
        print("GNU/Linux")
        return
    
    print(platform.system())

if __name__ == "__main__":
    main()