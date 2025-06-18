import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
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


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

# Generate content using the Gemini model
response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=[system_prompt])
)

# Response handling
answer = response.text
function_calls = response.function_calls
function_call_part = response.function_calls[0]

# Set up the function to call functions based on prompts

def call_function(function_call_part, verbose=False):
    # 1. Check if function exists
    function_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    if function_call_part.name not in function_dict:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=function_call_part.name,
                response={
                    "error": f"Unknown function: {function_call_part.name}"}
            )
            ],
        )
        
    if response.function_calls and len(response.function_calls) > 0:
        function_call_result = call_function(function_call_part, verbose=...)
        print("->", function_call_result.parts.function_response.response["result"])
        print(function_call_result.parts)

    # 2. Prepare arguments for function call
    function_object = function_dict[function_call_part.name]
    function_args = dict(function_call_part.args)
    function_args["working_directory"] = './calculator'
    function_result = function_object(**function_args)
    if "--verbose" in sys.argv[2:]:
        print(
            f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f"Calling function: {function_call_part.name}")

    # 3. Call function and gather result
    try:
        function_result = function_dict[function_call_part.name](**function_args)
    except Exception as e:
        function_result = f"Error: {e}"
    # 4. Construct Content object with the response
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result}
        )],
    )


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
