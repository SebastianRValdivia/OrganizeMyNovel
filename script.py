import argparse
import yaml
import os
import subprocess

# GLOBALS
novel_dir: str
settings: dict


# MAIN FUNCTIONS
def init_scene():
    last_chapter = get_last_chapter()
    last_scene = get_last_scene_of_chapter(last_chapter)
    scene_path = create_folder(f"./chapters/{last_chapter}/", str(last_scene+1))
    create_file(scene_path, "text.txt")
    create_file(scene_path, "meta.yml")

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

def init_chapter():
    """Create a chapter by 1"""
    last_chapter = get_last_chapter()
    try:
        chapters_path = os.path.join(novel_dir, "chapters", str(
            int(last_chapter) + 1)
        )
        os.makedirs(chapters_path)

    except OSError as e:
        print(f"Error: {e}")

# UTILS
def go_to_novel_dir():
    """Set the working directory back to the novel root dir"""
    os.chdir(novel_dir)

def get_last_scene_of_chapter(chapter_num: int):
    """Retrieve the chapter number and the scene number of the last scene"""
    last_chapter_folder = f"./chapters/{chapter_num}/"
    try:
        os.chdir(last_chapter_folder)  # Change directory to the provided base folder

        highest_folder_number = -1  # Initialize the highest folder number
        folders = [folder for folder in os.listdir() if os.path.isdir(folder) and folder.isdigit()]
        
        # Iterate through the list of folders and find the highest numbered folder
        for folder in folders:
            folder_number = int(folder)
            if folder_number > highest_folder_number:
                highest_folder_number = folder_number

        go_to_novel_dir()
        return highest_folder_number

    except OSError as e:
        print(f"Error: {e}")
        return None

def create_folder(folder_path, folder_name):
    try:
        full_path = os.path.join(folder_path, folder_name)
        os.makedirs(full_path)
        print(f"Folder '{folder_name}' created successfully at '{folder_path}'.")
        return full_path

    except OSError as e:
        print(f"Error: {e}")

def create_file(file_path, file_name):
    try:
        full_file_path = os.path.join(file_path, file_name)
        open(full_file_path, 'w').close()

        print(f"File '{file_name}' created successfully at '{file_path}'.")
        return full_file_path

    except OSError as e:
        print(f"Error: {e}")

def get_last_chapter():
    """Retrieve the last chapter number"""
    chapters_dir = "./chapters"

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
        return sorted_folders[0]
    else:
        print("No numbered folders found in the chapters directory.")
        return None


def load_settings():
    """
    Load the settings from the settings.yml file in the root of the novel dir
    """
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
            # Init new scene
            init_scene()
        elif (args.task[0] == "nextchapter"):
            # Get last chapter
            # Init chapter
            init_chapter()
        else:
            raise Exception("Wrong command") 





