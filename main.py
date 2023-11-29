import argparse
import os
import subprocess

novel_dir: str


def init_chapter(chapter_number: int):
    chapter_dir = f"{novel_dir}/chapters/{chapter_number}/"
    os.makedirs(chapter_dir)
    print(f"Chapter {chapter_number} started")
    go_to_novel_dir()

def init_scene(chapter_number:int, scene_number: int):
    scene_dir = f"{novel_dir}/chapters/{chapter_number}/{scene_number}/"
    os.makedirs(scene_dir)
    os.chdir(scene_dir)
    open("text.txt", "w").close()
    open("meta.yml", "w").close()

    go_to_novel_dir()

def init_novel(novel_name: str):
    """
    Initialize a new novel, start git and create the main folders.
    All hidden funcs are mean to be run only on initializaiton.
    """
    def _init_git():
        """
        Run 'git init' command on the folder
        """ 
        subprocess.run(['git', 'init'])
        print('Git repository initialized.')

    def _init_settings():
        try:
            os.mknod('settings.yml')
        except FileExistsError:
            print('Error: Already in a novel.')

    def _init_folders():
        folders_needed = ["./chapters", "./docs/characters", ]
        for folder_name in folders_needed:
            os.makedirs(folder_name)
            print(f"Folder '{folder_name}' created successfully.")
    def _init_first_chapter():
        chapter_dir = f"{novel_dir}/chapters/0/"
        os.makedirs(chapter_dir)
    def _init_first_scene():
        scene_dir = f"{novel_dir}/chapters/0/0/"
        os.makedirs(scene_dir)
        os.chdir(scene_dir)
        open("text.txt", "w").close()
        open("meta.yml", "w").close()

    try:
        os.makedirs(novel_name)
        print('Novel folder created successfully.')
    except OSError:
        print('Error creating folder')
        exit()

    # Go to new dir and re-set the novel_dir
    os.chdir(novel_name)
    novel_dir = os.getcwd()
    # Init stuff
    _init_git()
    _init_settings()
    _init_folders()
    _init_first_chapter()
    _init_first_scene()

# UTILS
def go_to_novel_dir():
    """Set the working directory back to the novel root dir"""
    os.chdir(novel_dir)




if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Organize my novel')
    parser.add_argument('task', nargs='*', help='Task to do')
    args = parser.parse_args()

    novel_dir = os.getcwd()

    # Manage input
    if not any(vars(args).values()): # No args at all
        print("no args") # To be replaced with ui
    else:
        if (args.task[0] == 'create'): # Create new novel
            try:
                novel_name = args.task[1]
                init_novel(novel_name)
            except IndexError:
                print('Missing novel name') 
        else:
            raise Exception('Wrong command') 





