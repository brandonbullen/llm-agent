import os
import subprocess

from pathlib import Path
from functions.config import MAX_CHARACTERS
from google.genai import types

# Set function declaration for LLM
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a file within the working directory up to 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read the content from, relative to the working directory."
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python script through the subprocess library and returns it's output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be executed with the subprocess command, if not a python file error."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="An optional list of strings that will be passed as arguments into the python script."
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Receives a path to create a file and the content to populate that file, with respects to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the desired file to be created, with respect to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content string to write/overwrite the file_path with."
            )
        }
    )
)

# Some helper functions we are using often.
def build_full_path(working_directory, directory="."):
    return os.path.abspath(os.path.join(working_directory, directory))

def in_working_directory(path, working_directory):
    return path.startswith(os.path.abspath(working_directory))

# LLM Functions
def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    if not in_working_directory(full_path, working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    

    dir_contents = os.listdir(full_path)
    file_list = []
    for item in dir_contents:
        item_path = f'{full_path}/{item}'
        file_list.append(f'- {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}')
    return "\n ".join(file_list)

def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    file_too_long = f'[...File "{file_path}" truncated at 10000 characters]'

    if os.path.isdir(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    if not in_working_directory(full_path, working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(full_path):
        with open(full_path, "r") as f:
            file_content = f.read(MAX_CHARACTERS)
            if len(file_content) == 10000:
                return file_content + '\n' + file_too_long
            return file_content
    else:
        return f'Error: File not found or is not a regular file: "{file_path}"'

def write_file(working_directory, file_path, content):
    full_path = build_full_path(working_directory, file_path)

    if not in_working_directory(full_path, working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists('/'.join(full_path.split('/')[:-1])):
        os.makedirs('/'.join(full_path.split('/'[:-1])))
    
    with open(full_path, 'w') as f:
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    
def run_python_file(working_directory, file_path, args=[]):
    full_path = build_full_path(working_directory, file_path)

    if not in_working_directory(full_path, working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if os.path.splitext(full_path)[1] != ".py":
        f'Error: "{file_path}" is not a Python file.'

    full_command = ["python3", full_path] + args
    try:
        result = subprocess.run(
            full_command,
            cwd=working_directory,
            timeout=30,
            capture_output=True
        )

        if result:
            pretty_print = [
                f'STDOUT: {result.stdout}',
                f'STDERR: {result.stderr}',
            ]
            
            if result.returncode == 0:
                pretty_print.append(f'Process exited with code {result.returncode}')

            return '\n'.join(pretty_print)
        else:
            return 'No output produced.'
    except Exception as e:
        return f"Error: executing Python file: {e}"
