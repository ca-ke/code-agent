from google.genai import types
from functions.write_file import write_file

def create_plan(working_directory, tasks, goal, filename):
    content = """""" + "\n" 
    content += f"# Plan to {goal}\n\n"
    content += "## Tasks\n\n"
    for task in tasks:
        content += f"- [ ] {task}\n"

    file_path = f"plan/{filename}.md"
    
    write_file(working_directory, file_path, content)
    return f'Plan created and written to "{file_path}" with {len(tasks)} tasks.'


schema_create_plan = types.FunctionDeclaration(
    name="create_plan",
    description="Create a markdown plan file with a list of tasks to achieve a specified goal.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "tasks":types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="A list of tasks to include in the plan.",
            ),
            "goal":types.Schema(
                type=types.Type.STRING,
                description="The overall goal that the plan is designed to achieve.",
            ),
            "filename":types.Schema(
                type=types.Type.STRING,
                description="The name of the markdown file (without extension) to create for the plan.",
            )
        }
    )
)

