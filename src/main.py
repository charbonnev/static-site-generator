import os
import shutil
from textnode import *

def erase_all_files_from_directory(directory):
    # erase all from directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def copy_all_files(source, destination):
    root, dirs, files = os.walk(source)
    for dir in dirs:
        shutil.copytree(os.path.join(root, dir), os.path.join(destination, dir))
    for file in files:
        shutil.copy(os.path.join(root, file), destination)

def main():
    erase_all_files_from_directory("public")
    copy_all_files("static", "public")
    


if __name__ == "__main__":
    main()