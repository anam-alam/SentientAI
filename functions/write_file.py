import os, config
from pathlib import Path
from google.genai import types

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
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a file’s contents within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Directory to run the command from."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file where contents need to be written, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file."
            ),
        },
        required=["working_directory","file_path","content"]
    ),
)
