import os
import typer

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.utils import minify_string

from config import system_prompt, available_functions

load_dotenv()

app = typer.Typer()

@app.command()
def main(prompt: str = typer.Argument(..., help="The prompt to send to the LLM"),
         working_directory: str = typer.Option(".", help="The working directory for file operations"),
         verbose: bool = typer.Option(False, help="Enable verbose output")):
    """
    A script that interacts with LLM.
    """

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    iteration = 0
    while iteration < 20:
        try:
            llm_response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=minify_string(system_prompt),
                    tools=[available_functions]
                ),
            )
            messages = process_llm_response(llm_response, messages, working_directory, verbose, prompt, iteration)
            if messages is None:
                break
            iteration+=1

        except Exception as e:
            print(f"Error: {e}")
            break
    print_messages(messages)


def process_llm_response(llm_response, messages, working_directory, verbose, prompt, iteration):
    # Process candidate responses from the LLM
    if llm_response.candidates is not None:
        for candidate in llm_response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    # Process function calls from the LLM
    if llm_response.function_calls:
        for function_call in llm_response.function_calls:
            call_function_response = call_function(function_call, working_directory, verbose=verbose)
            if not isinstance(call_function_response, types.Content):
                raise RuntimeError("call_function must return a Content object")
            parts = call_function_response.parts or []
            if not parts:
                raise RuntimeError("call_function must return a Content object with at least one Part")

            func_response = getattr(parts[0], "function_response", None)
            if not func_response or not getattr(func_response, "response", None):
                raise RuntimeError("call_function must return a Content object with a Part containing a FunctionResponse with a response")
            messages.append(types.Content(role="tool", parts=[types.Part(function_response=parts[0].function_response)]))
            if verbose:
                print_function_call_result(func_response)

    # If the LLM provides a final text response (without function calls), print it and end the interaction
    has_function_calls = llm_response.function_calls is not None
    if llm_response.text and not has_function_calls:
        print(f"Final response after {iteration} iterations:\n{llm_response.text}")
        return None

    # If verbose mode is enabled, print usage metadata
    if verbose and llm_response.usage_metadata:
        print_usage_metadata(prompt, llm_response.usage_metadata)
    return messages


def print_function_call_result(func_response):
    print(f"-> {func_response.response['result']}")

def print_usage_metadata(prompt, usage_metadata):
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
    print(f"Response tokens: {usage_metadata.candidates_token_count}")

def print_messages(messages):
    if not messages:
        return
    for message in reversed(messages):
        role = message.role
        parts = message.parts or []
        for part in parts:
            if part.text:
                print(f"{role}: {part.text}\n")
            if part.function_response:
                func_resp = part.function_response
                print(f"{role} called function {func_resp.name} with response: {func_resp.response}\n")

if __name__ == "__main__":
    app()
