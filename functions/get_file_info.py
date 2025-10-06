import os
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    if os.path.abspath(working_directory) not in os.path.abspath(full_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with(open(full_path, "r")) as f:
            content = f.read(MAX_CHARS)
            content += f"[...File {file_path} truncated at {MAX_CHARS} characters]"
    except Exception as e:
        return f'Error: reading file "{file_path}": {e}'
    return content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            )
        }
    )
)

