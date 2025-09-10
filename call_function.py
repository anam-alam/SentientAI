import os
import google.genai.types as types
from functions.get_files_info import *
from functions.write_file import write_file,schema_write_file
from functions.run_python_file import run_python_file,schema_run_python_file
from functions.get_file_content import get_file_content,schema_get_file_content
import config


working_directory = "./calculator"

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

callable_functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part:types.FunctionCall, verbose=False):
    function_name = function_call_part.name
    if not function_name:
        print(f"Error: function has no name")

    function_args = dict(function_call_part.args)
    function_args["working_directory"] = "./calculator"

    #print("HI",function_args)

    if not function_args:
        print(f"Error: function \"{function_name}\" has no arguments")
        
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    try:
        func_to_run = callable_functions[function_name]
    except KeyError:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_result = func_to_run(**function_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
