import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERATIONS


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python3 main.py "<prompt>" [--verbose]')
        print('Example: python3 main.py "What is the meaning of life?" --verbose')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)

    # Validate the verbose flag
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    # Create a new list to store messages and prompts
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    counter = 0
    while True:
        counter += 1

        if counter > MAX_ITERATIONS:
            print(
                f"Maximum number of iterations ({MAX_ITERATIONS}) reached. Exiting...")
            sys.exit(1)

        final_response = generate_content(client, messages, verbose)
        try:
            if final_response:
                print("Final response:")
                print(final_response, "\n")
                break
        except Exception as e:
            print(
                f"Error in generating content: {e}")


def generate_content(client, messages, verbose):
    # Generate content using the Gemini model
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=[system_prompt]
        ),
    )

    # Response handling
    answer_text = response.text
    function_calls = response.function_calls
    candidates = response.candidates

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if candidates:
        for candidate in candidates:
            candidate_content = candidate.content
            messages.append(candidate_content)

    if not function_calls:
        return answer_text

    call_responses = []
    for function_call_part in function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Error: empty function call result returned")
        if verbose:
            print(
                f"-> {function_call_result.parts[0].function_response.response}")
        return call_responses.append(function_call_result.parts[0])

    if not call_responses:
        raise Exception("Error: no function responses generated")

    messages.append(types.Content(
        role="tool",
        parts=call_responses
    ))


if __name__ == "__main__":
    main()
