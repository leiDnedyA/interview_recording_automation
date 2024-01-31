import os
import shutil
import argparse
import dotenv
import subprocess
from datetime import datetime

dotenv.load_dotenv()

source_directory = os.getenv("SOURCE_DIRECTORY")
destination_directory = os.getenv("DESTINATION_DIRECTORY")
target_file_substring = os.getenv("TARGET_FILE_SUBSTRING") # substring of file in target subdirectory
remotasks_email = os.getenv("REMOTASKS_EMAIL")

def open_file_explorer(directory):
    try:
        subprocess.Popen(["open", directory])
    except Exception as e:
        print(f'Error: {e}')

def get_formatted_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    return formatted_date

def search_and_copy_file(source_dir, destination_dir, file_substring, user_email):
    for filename in os.listdir(source_dir):

        if file_substring.upper() in filename.upper():
            subdirectory_path = os.path.join(source_dir, filename)
            target_file_path = None

            try:
                # Iterate through subdirectory
                for filename in os.listdir(subdirectory_path):
                    print(filename)
                    if target_file_substring in filename:
                        target_file_path = os.path.join(subdirectory_path, filename)

                # Check to see if target file exists in target directory
                if (not target_file_path):
                    raise Exception(f"No file with substring '{target_file_substring}' in target directory '{subdirectory_path}'")

                output_filename = f'{get_formatted_date()}_{remotasks_email}_{user_email}.mp4'
                output_path = os.path.join(destination_directory, output_filename)

                # Copy the file to the destination directory
                shutil.copy(target_file_path, output_path)
                print(f"File '{target_file_path}' copied successfully as '{output_filename}'.")
            except FileNotFoundError:
                print(f"Error: File with substring '{target_file_substring}' not found in directory {subdirectory_path}.")
            except PermissionError:
                print(f"Error: Permission denied for file '{target_file_path}'.")
            except Exception as e:
                print(f"Error: {e}")
def main():
    parser = argparse.ArgumentParser(description="Search and copy files based on a substring in the file name.")
    parser.add_argument("directory_keyword", help="Substring to search for target directory.")
    parser.add_argument("user_email", help="Email to use in filename")

    args = parser.parse_args()

    search_and_copy_file(source_directory, destination_directory, args.directory_keyword, args.user_email)

    open_file_explorer(destination_directory)


if __name__ == "__main__":
    main()


