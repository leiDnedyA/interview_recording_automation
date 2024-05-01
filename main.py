#!/usr/bin/env -S /bin/sh -c '"$(dirname "$0")/venv/bin/python3" "$0" "$@"'

import os
import shutil
import argparse
import dotenv
import subprocess
import platform
import webbrowser
from datetime import datetime

dotenv.load_dotenv()

source_directory = os.getenv("SOURCE_DIRECTORY")
destination_directory = os.getenv("DESTINATION_DIRECTORY")
target_file_substring = os.getenv("TARGET_FILE_SUBSTRING") # substring of file in target subdirectory
remotasks_email = os.getenv("REMOTASKS_EMAIL")
google_drive_url = os.getenv("GOOGLE_DRIVE_URL")

source_directory = os.path.expanduser(source_directory)
destination_directory = os.path.expanduser(destination_directory)

def is_gnome_running():
  """Returns True if GNOME is running, False otherwise."""
  try:
    subprocess.call(["gnome-shell", "--version"])
    return True
  except subprocess.CalledProcessError:
    return False

def open_file_explorer(directory, filename=None):
    try:
        # If running in gnome environment, open nautilus and select file
        if is_gnome_running() and filename: 
            subprocess.Popen(["nautilus", os.path.join(directory, filename)])
            return
        subprocess.Popen(["open", directory])
    except Exception as e:
        print(f'Error: {e}')

def get_formatted_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    return formatted_date

def search_and_copy_file(source_dir, destination_dir, file_substring, output_filename):
    """ Searches for and copies recording file. Returns 0 if successful and 1 otherwise. """
    for filename in os.listdir(source_dir):
        if file_substring.upper() in filename.upper():
            subdirectory_path = os.path.join(source_dir, filename)
            target_file_path = None

            try:
                # Iterate through subdirectory
                for filename in os.listdir(subdirectory_path):
                    if target_file_substring in filename:
                        target_file_path = os.path.join(subdirectory_path, filename)

                print(target_file_path)
                # Check to see if target file exists in target directory
                if (not target_file_path):
                    raise Exception(f"No file with substring '{target_file_substring}' in target directory '{subdirectory_path}'")

                output_path = os.path.join(destination_directory, output_filename)

                # Copy the file to the destination directory
                shutil.copy(target_file_path, output_path)
                print(f"File '{target_file_path}' copied successfully as '{output_filename}'.")
                return 0
            except FileNotFoundError:
                print(f"Error: File with substring '{target_file_substring}' not found in directory {subdirectory_path}.")
            except PermissionError:
                print(f"Error: Permission denied for file '{target_file_path}'.")
            except Exception as e:
                print(f"Error: {e}")
    return 1

def main():
    parser = argparse.ArgumentParser(description="Search and copy files based on a substring in the file name.")
    parser.add_argument("directory_keyword", help="Substring to search for target directory.")
    parser.add_argument("user_email", help="Email to use in filename")

    args = parser.parse_args()

    output_filename = f'{get_formatted_date()}_{remotasks_email}_{args.user_email}.mp4'

    result = search_and_copy_file(source_directory, destination_directory, args.directory_keyword, output_filename)

    if result != 0:
        print('Error: there was a problem.')
        return

    open_file_explorer(destination_directory, output_filename)
    webbrowser.open(google_drive_url)


if __name__ == "__main__":
    main()


