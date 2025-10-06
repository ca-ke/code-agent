from functions.get_file_info import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_file import run_python_file
from functions.create_plan import create_plan
from functions.update_plan import update_plan
from google.genai import types

def call_function(function_call_part, working_directory, verbose=False):
    kwargs = dict(function_call_part.args)
    kwargs["working_directory"] = working_directory
    if verbose:
        print(f"Calling function: {function_call_part.name}({kwargs})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    functions = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
        "create_plan": create_plan,
        "update_plan": update_plan,
    }
    function_name = function_call_part.name
    function = functions.get(function_name)
    if not function:
        return  types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        ) 
    result = function(**kwargs)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ]
    )
