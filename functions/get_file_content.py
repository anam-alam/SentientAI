from config import MAX_CHARS
import os
from google.genai import types

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
    


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents in a specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            # "working_directory": types.Schema(
            #     type=types.Type.STRING,
            #     description="The directory to list file's content from, relative to the working directory.",
            # ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file whose contents to read, relative to the working directory."
            ),
        },
        required=["file_path"]
    ),
)


