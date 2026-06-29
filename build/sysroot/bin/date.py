from datetime import datetime

def main():
    now = datetime.now().astimezone()
    print(now.strftime("%a %d %Y %I:%M:%S %p %Z"))

if __name__ == "__main__":
    main()