import os, config
from pathlib import Path

def write_file(working_directory, file_path, content):
    #print(file_path)
    full_path = os.path.join(working_directory,file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(full_path)

    if not abs_target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    
    if not os.path.exists(abs_target_dir):
        try:
            os.makedirs(os.path.dirname(abs_target_dir), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(abs_target_dir) and os.path.isdir(abs_target_dir):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(abs_target_dir, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: writing to file: {e}"