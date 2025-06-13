import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

# Generate content using the Gemini model
response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=messages,
)

answer = response.text
# Print the response text
print(f"Response: {answer}")

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

