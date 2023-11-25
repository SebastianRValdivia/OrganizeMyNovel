import os
import subprocess

def init(novel_name):
    try:
        os.makedirs(novel_name)
        print('Novel folder created successfully.')
        os.chdir(novel_name)

        # Run 'git init' command
        subprocess.run(["git", "init"])
        print(f"Git repository initialized.")

    except OSError as e:
        print(f'Error: {e}')
