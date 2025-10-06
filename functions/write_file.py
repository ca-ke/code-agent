import os
from google.genai import types

def write_file(working_directory, file_path, content):
    fullpath = os.path.join(working_directory, file_path)    
    if os.path.abspath(working_directory) not in os.path.abspath(fullpath):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(fullpath):
        dir_name = os.path.dirname(fullpath)
        if dir_name and not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name)
            except Exception as e:
                return f'Error: creating directories for "{file_path}": {e}'

    try:
        with(open(fullpath, "w")) as f:
            f.write(content)
    except Exception as e:
        return f'Error: writing file "{file_path}": {e}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_python_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a specified file within the working directory, creating directories as needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            )
        }
    )
)
