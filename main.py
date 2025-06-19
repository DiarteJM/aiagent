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


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
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

    agent_count = 0
    # while agent_count <= 20:
    response = generate_content(client, messages, verbose)
    candidates = response.candidates 
    print(f"Candidate Type: {type(candidates)}")

        # check the .candidates property of the response - should be a list of response variations
    # if candidates is None:
    #     print("No candidates found. Exiting.")
    #     break
        # iterate through the candidates and print their text
        # for candidate in candidates:
        #     if verbose:
        #         print(f"Candidate {agent_count + 1}: {candidate.text}")
        #     messages.append(types.Content(role="tool", parts=[types.Part(text=candidate.text)]))
            # if verbose, print the candidate text
            # append the candidate text to the messages list
            # this is to ensure that the next iteration of generate_content has the full conversation history


        # agent_count += 1
        # after each function call, append the returned types.Content to the messages list
        # if function called, should iterate again (unless max iterations is reached) - else print the final response (.text property) and break out of loop
        # ensure with each call to run the generate_content function, the messages list has to be passed in so LLM does the next step


if __name__ == "__main__":
    main()
