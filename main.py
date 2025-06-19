import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from system_prompt import system_prompt
from functions.call_function import available_functions, call_function


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
    answer = response.text
    function_calls = response.function_calls

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not function_calls:
        return f"Response: {answer}"

    call_responses = []
    for function_call_part in function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (not function_call_result.parts or not function_call_result.parts[0].function_response):
            raise Exception("Error: You have an empty call result")
        if verbose:
            print(
                f"-> {function_call_result.parts[0].function_response.response}")
        return call_responses.append(function_call_result.parts[0])

    if not call_responses:
        raise Exception(
            "Error: no function responses generated. Please check your function calls or try again.")
        
    messages.append(
        types.Content(
            role="tool",
            parts=call_responses,
        )
    )


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

    generate_content(client, messages, verbose)

    prompt_counter = 0
    while True:
        prompt_counter += 1

        if prompt_counter > 20:
            print(
                f"Stopping after {prompt_counter} prompts to avoid infinite loop.")
            sys.exit(1)
        try:
            response = generate_content(client, messages, verbose)

            if response:
                print("Response:")
                print(response, "\n")
                break
        except BaseException as e:
            print(
                f"Error in generating content for prompt {prompt_counter}: {e}")
            # Continue to next prompt

        user_input = input(f"Prompt {prompt_counter}: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the AI Code Assistant.")
            break

        messages.append(types.Content(
            role="user", parts=[types.Part(text=user_input)]))
        response = generate_content(client, messages, verbose)
        print(response)


if __name__ == "__main__":
    main()
