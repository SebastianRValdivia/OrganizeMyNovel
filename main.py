import argparse
from scripts.creation import init

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Organize my novel')
    parser.add_argument('task', nargs='*', help='Task to do')
    args = parser.parse_args()

    if not any(vars(args).values()): # No args at all
        print("no args") # To be replaced with ui
    else:
        if (args.task[0] == 'create'):
            try:
                novel_name = args.task[1]
                init(novel_name)
            except IndexError:
                print('Missing novel name') 
        else:
            raise Exception('Wrong') 





