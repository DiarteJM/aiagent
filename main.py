import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
  
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("Error: No prompt was entered. Please try again in the command line interface.")
    sys.exit(1)
else:
    user_prompt = " ".join(sys.argv[1:])

# Create a new list to store messages and prompts
messages = [
  types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Create the declaration for the schema for the functions
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
    description="Retrieves the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, creating the file if it does not exist, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Generate content using the Gemini model
response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt)
    )

answer = response.text
# print(f"Response: {answer}")
function_calls = response.function_calls
# print(f"Function Calls: {response.function_calls}")

if function_calls and len(function_calls) > 0:
    fc = function_calls[0]
    function_name = fc.name
    function_args = fc.args
    print(f"Calling function: {function_name}({function_args})")

    if function_name == "get_files_info":
        from functions.get_files_info import get_files_info
        result = get_files_info(working_directory=os.getcwd(), directory=function_args.get("directory", "."))
        print(result)
    elif function_name == "get_file_content":
        from functions.get_file_content import get_file_content
        result = get_file_content(working_directory=os.getcwd(), file_path=function_args.get("file_path"))
        print(result)
    elif function_name == "run_python_file":
        from functions.run_python import run_python_file
        result = run_python_file(working_directory=os.getcwd(), file_path=function_args.get("file_path"))
        print(result)
    elif function_name == "write_file":
        from functions.write_file import write_file
        result = write_file(working_directory=os.getcwd(), file_path=function_args.get("file_path"), content=function_args.get("content", "."))
        print(result)
    else:
        if function_name not in function_calls:
          print(f"Error: Function '{function_name}' is not supported.")
          sys.exit(1)
else:
    print(answer)


# Print the token usage metadata
prompt_token_usage = response.usage_metadata.prompt_token_count
response_token_usage = response.usage_metadata.candidates_token_count

if sys.argv[2:].__contains__('--verbose'):
  user_prompt = user_prompt.replace(" --verbose", "")
  print(f"User prompt: '{user_prompt}'")
  print(f"Prompt tokens: {prompt_token_usage}")
  print(f"Response tokens: {response_token_usage}")
else:
  print(f"{answer}")

