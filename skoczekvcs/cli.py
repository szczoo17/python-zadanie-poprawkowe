import skoczekvcs
import argparse


def main():
    parser = argparse.ArgumentParser(description='Version control system')
    parser.add_argument('src', metavar='<source>')
    parser.add_argument('dest', metavar='<destination>')
    args = parser.parse_args()

    r = skoczekvcs.Repository(args.src, args.dest)
    quit = False
    while not quit:
        command = input("> ")
        words = command.split()
        if command == 'help':
            print("commit - new revision")
            print("restore <n> - restore revision number <n>")
            print("revision - prints the latest revision number")
            print("quit - quits")
            print("help - helps")
        elif command == 'commit':
            r.commit()
        elif words[0] == 'restore':
            number = None
            if len(words) == 1:
                number = input("Which revision do you want to restore? ")
            else:
                number = words[1]
            if not number.isdigit():
                print("Argument must be a number")
            else:
                r.restore(int(number))
        elif command == 'revision':
            print("Latest revision number is {}".format(r.getRevision()))
        elif command == 'quit':
            quit = True
        else:
            print("Unknown command. Type 'help' for the list of commands")


if __name__ == '__main__':
    main()
