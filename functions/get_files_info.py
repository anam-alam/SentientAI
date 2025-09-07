import os


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory,directory)
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(full_path)

    if not abs_target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_target_dir):
        return f'Error: "{directory}" is not a directory'
    
    try:
        entries = []
        for name in os.listdir(abs_target_dir):
            path = os.path.join(abs_target_dir, name)
            if name == "__pycache__":
                continue
            is_dir = os.path.isdir(path)
            size = os.path.getsize(path)
            entries.append(f"{name}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(entries)
    except Exception as e:
        return f'Error: {e}'
    



