import os

from google.genai import types


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    label = "current" if directory == "." else directory
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        body = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        result = f"Result for {label} directory:\n    {body}"
        return result

    if not os.path.isdir(full_path):
        body = f'Error: "{directory}" is not a directory'
        result = f"Result for {label} directory:\n    {body}"
        return result

    try:
        items = os.listdir(full_path)
        items.sort()
        results = []
        for item in items:
            item_path = os.path.join(full_path, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            results.append(f"    - {item}: file_size={size} bytes, is_dir={is_dir}")
    except Exception as e: 
        return f'Result for {label} directory:\n    Error: {e}'

    body = "\n".join(f"{line}" for line in results)
    result = f"Result for {label} directory:\n{body}"
    return result

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Get information about files in a specified directory within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory":types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Use '.' for the current working directory.",
            )
        }
    )
)
