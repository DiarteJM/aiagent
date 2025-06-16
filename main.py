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

# Create the declaration for the schema for get_files_info function
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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Generate content using the Gemini model
response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt)
    )

answer = response.text
# print(f"Response: {answer}")
function_call = response.function_calls
# print(f"Function Calls: {response.function_calls}")

if function_call and len(function_call) > 0:
    fc = function_call[0]
    function_name = fc.name
    function_args = fc.args
    print(f"Calling function: {function_name}({function_args})")
    if function_name != "get_files_info":
        print(f"Error: Function '{function_name}' is not supported.")
        sys.exit(1)
    else:
        from functions.get_files_info import get_files_info
        result = get_files_info(working_directory=os.getcwd(), directory=function_args.get("directory", "."))
        print(result)
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

