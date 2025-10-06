
import os

from google.genai import types

import logging
import tempfile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_plan(working_directory, plan_name, task_description):
    wd = os.path.realpath(working_directory)
    plan_path = os.path.join(wd, "plan", f"{plan_name}.md")

    logging.info(f"Updating plan at: {plan_path}")

    if not isinstance(plan_name, str) or not plan_name:
        logging.error("Error: plan_name must be a non-empty string.")
        return False
    if not isinstance(task_description, str) or not task_description:
        logging.error("Error: task_description must be a non-empty string.")
        return False

    try:
        if not os.path.exists(plan_path):
            logging.error(f"Error: Plan file '{plan_path}' not found.")
            return False

        with open(plan_path, "r") as f:
            plan_content = f.read()

        task_string = f"- [ ] {task_description}"
        if task_string in plan_content:
            updated_task_string = f"- [x] {task_description}"
            updated_plan_content = plan_content.replace(task_string, updated_task_string, 1)

            with tempfile.NamedTemporaryFile(mode="w", delete=False, dir="plan", suffix=".md") as tmp_file:
                tmp_file.write(updated_plan_content)
                temp_file_name = tmp_file.name

            os.replace(temp_file_name, plan_path)

            logging.info(f"Task '{task_description}' updated in {plan_path}")
            return True
        elif f"- [x] {task_description}" in plan_content:
            logging.info(f"Task '{task_description}' already completed.")
            return True
        else:
            logging.warning(f"Task '{task_description}' not found in {plan_path}")
            return False

    except Exception as e:
        logging.exception(f"An error occurred: {e}")
        return False

schema_update_plan = types.FunctionDeclaration(
    name="update_plan",
    description="Mark a task as completed in the plan file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "plan_name": types.Schema(
                type=types.Type.STRING,
                description="The name of the plan file located in the 'plan' directory.",
            ),
            "task_description": types.Schema(
                type=types.Type.STRING,
                description="The exact description of the task to be marked as completed.",
            ),
        },
    ),
)
