import os
import subprocess

def _init_git():
    # Run 'git init' command
    subprocess.run(["git", "init"])
    print("Git repository initialized.")


def init(novel_name):
    try:
        os.makedirs(novel_name)
        print('Novel folder created successfully.')
        os.chdir(novel_name)

        _init_git()


    except OSError as e:
        print(f'Error: {e}')
