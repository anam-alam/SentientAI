from config import MAX_CHARS
import os

def get_file_content(working_directory, file_path):
    #print(MAX_CHARS)
    full_path = os.path.join(working_directory,file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(full_path)

    if not abs_target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_target_dir):
        f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_target_dir) as f:
            file_content_string = f.read(MAX_CHARS)
        return file_content_string

    except Exception as e:
        return f'Error: {e}'