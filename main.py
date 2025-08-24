#! /usr/bin/python3

import argparse
import os
import sys

from google import genai
from google.genai import types
from dotenv import load_dotenv

from functions.get_files_info import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from functions.get_files_info import get_files_info, get_file_content, run_python_file, write_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

parser = argparse.ArgumentParser(
    prog='AI Code Assistant',
    description='Takes prompts and passes them to an LLM.'
)

parser.add_argument('user_prompt')
parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def main():
    load_dotenv()

    if not args.user_prompt:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Maybe we keep this for later?
    # user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]

    generate_content(client, messages)  
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")


def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    if response.function_calls:
        for call in response.function_calls:
            result = call_function(call)
            if result.parts[0].function_response.response:
                print(f"-> {result.parts[0].function_response.response}")
            else:
                raise Exception(f'Error making requested function call.')
    else:
        print(response.text)
    
    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_call_part.args["working_directory"] = "./calculator"

    if function_call_part.name not in ["get_files_info", "get_file_content", "run_python_file", "write_file"]:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    if function_call_part.name == "get_files_info":
        result = get_files_info(**function_call_part.args)
    if function_call_part.name == "get_file_content":
        result = get_file_content(**function_call_part.args)
    if function_call_part.name == "run_python_file":
        result = run_python_file(**function_call_part.args)
    if function_call_part.name == "write_file":
        result = write_file(**function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )



if __name__ == "__main__":
    main()
