import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

from config import system_prompt, available_functions

load_dotenv()

def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else sys.exit(1)
    argument = sys.argv[2] if len(sys.argv) > 2 else ""
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    iteration = 0
    while iteration < 20:
        try:
            content_response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages, 
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt, 
                    tools=[available_functions]
                ),
            )
  
            if content_response.candidates is not None: 
                for candidate in content_response.candidates:
                    if candidate.content:
                        messages.append(candidate.content)

            if content_response.function_calls:
                for function_call in content_response.function_calls:
                    call_function_response = call_function(function_call, verbose=(argument == "--verbose"))
                    if not isinstance(call_function_response, types.Content):
                        raise RuntimeError("call_function must return a Content object")
                    parts = call_function_response.parts or []
                    if not parts:
                        raise RuntimeError("call_function must return a Content object with at least one Part")

                    func_response = getattr(parts[0], "function_response", None)
                    if not func_response or not getattr(func_response, "response", None):
                        raise RuntimeError("call_function must return a Content object with a Part containing a FunctionResponse with a response")
                    messages.append(types.Content(role="tool", parts=[types.Part(function_response=parts[0].function_response)]))
                    if argument == "--verbose":
                        print(f"-> {func_response.response['result']}")
            
            has_function_calls = content_response.function_calls is not None
            if content_response.text and not has_function_calls:
                print(f"Final response after {iteration} iterations:\n{content_response.text}")
                break

            if argument == "--verbose" and content_response.usage_metadata:
                print(f"User prompt: {prompt}")
                print(f"Prompt tokens: {content_response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {content_response.usage_metadata.candidates_token_count}")
            iteration+=1
        except Exception as e:
            print(f"Error: {e}")
            break

    print_messages(messages)



def print_messages(messages):
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
    main()



