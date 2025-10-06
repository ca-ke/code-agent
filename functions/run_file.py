import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    if args is None:
        args = []
    wd = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(wd, file_path))

    if not full_path.startswith(wd + os.sep) and full_path != wd:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python", file_path, *args],
            capture_output=True,
            text=True,
            cwd=wd,
            timeout=30
        )
        parts = []
        if result.stdout:
            parts.append(f"\nSTDOUT:\n{result.stdout}")
        if result.stderr:
            parts.append(f"\nSTDERR:\n{result.stderr}")
        if result.returncode != 0:
            parts.append(f"Process exited with code {result.returncode}.")

        return "".join(parts) if parts else "No output produced."

    except subprocess.TimeoutExpired as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a specified Python file within the working directory and return its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args":types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="A list of arguments to pass to the Python file during execution.",
            )
        }
    )
)
