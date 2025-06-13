import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
  
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("Error: No prompt was entered. Please try again in the command line interface.")
    sys.exit(1)
else:
    prompt_input = " ".join(sys.argv[1:])

# Generate content using the Gemini model
response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=prompt_input,
)

answer = response.text
# Print the response text
print(f"Response: {answer}")

# Print the token usage metadata
prompt_token_usage = response.usage_metadata.prompt_token_count
response_token_usage = response.usage_metadata.candidates_token_count

print(f"Prompt tokens: {prompt_token_usage}")
print(f"Response tokens: {response_token_usage}")

