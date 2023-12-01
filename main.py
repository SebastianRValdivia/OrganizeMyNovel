import argparse
import yaml
import os
import subprocess

# GLOBALS
novel_dir: str
settings: dict


# MAIN FUNCTIONS
def init_chapter(chapter_number: int):
    chapter_dir = f"{novel_dir}/chapters/{chapter_number}/"
    os.makedirs(chapter_dir)
    print(f"Chapter {chapter_number} started")

def init_scene(chapter_number:int, scene_number: int):
    scene_dir = f"{novel_dir}/chapters/{chapter_number}/{scene_number}/"
    os.makedirs(scene_dir)
    os.chdir(scene_dir)
    open("text.txt", "w").close()
    open("meta.yml", "w").close()

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
    global novel_dir
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

def get_last_scene():
    """Retrieve the chapter number and the scene number of the last scene"""
    return [last_chapter_number, last_scene_number]

def get_last_chapter():
    """Retrieve the last chapter number"""
    chapters_dir = "./chapters"  # Path to the chapters folder

    # Check if the chapters folder exists
    if not os.path.exists(chapters_dir) or not os.path.isdir(chapters_dir):
        print("Chapters folder does not exist or is not a directory.")
        quit()

    # Get a list of directories in the chapters folder
    chapter_folders = [
        folder for folder in os.listdir(chapters_dir) if os.path.isdir(
            os.path.join(chapters_dir, folder
        ))
    ]

    # Filter and extract folders starting with a numeric value
    numeric_folders = [
        folder for folder in chapter_folders if folder.isdigit()
    ]

    # Sort the numeric folders in descending order (highest number first)
    sorted_folders = sorted(numeric_folders, key=int, reverse=True)

    if sorted_folders:
        # Return the folder with the highest number
        return os.path.join(chapters_dir, sorted_folders[0])
    else:
        print("No numbered folders found in the chapters directory.")
        return None


def load_settings():
    """
    Load the settings from the settings.yml file in the root of the novel dir
    """
    settings = {}
    with open('./settings.yml', 'r') as settings_file:
        settings = yaml.safe_load(settings_file)
    
    return settings




if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description="Organize my novel")
    parser.add_argument("task", nargs="*", help="Task to do")
    args = parser.parse_args()

    novel_dir = os.getcwd()

    # Manage input
    if not any(vars(args).values()): # No args at all
        print("no args") # To be replaced with ui
    else:
        if (args.task[0] == "create"): # Create new novel
            try:
                novel_name = args.task[1]
                init_novel(novel_name)
            except IndexError:
                print("Missing novel name") 
        elif (args.task[0] == "andscene"): # Create a new scene
            # Get last scene
            last_scene = get_last_scene()
            # Init new scene
            init_scene()
        elif (args.task[0] == "nextchapter"):
            # Get last chapter
            last_chapter = get_last_chapter()
            print(last_chapter)
            # Init chapter
            #init_chapter(get_last_chapter + 1)
        else:
            raise Exception("Wrong command") 





