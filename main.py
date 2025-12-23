import os
import argparse
from re import X
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions import call_functions


def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API Key not found")
    return api_key


def parse_args():
    parser = argparse.ArgumentParser(description="AI Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args


def prompt_ai(client, prompts):
    """prompt ai
    client: genai client
    prompts: [] list of messages to prompt with
    """

    available_functions = call_functions.available_functions
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompts,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )
    if not response:
        raise RuntimeError("failed API request")
    metadata = response.usage_metadata
    function_calls = response.function_calls
    return response, metadata, function_calls


def main():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    cli_args = parse_args()

    user_prompt = cli_args.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    response, metadata, function_calls = prompt_ai(client, messages)

    if cli_args.verbose:
        print(f"User prompt: {user_prompt}")
        print(
            f"Prompt tokens: {metadata.prompt_token_count}\nResponse tokens: {metadata.candidates_token_count}"
        )

    if function_calls:
        function_results = []
        for function_call in function_calls:
            function_call_result = call_functions.call_functions(function_call)
            if not function_call_result.parts:
                raise Exception("Error: parts (function_result.parts) is empty!")
            if not function_call_result.parts[0].function_response:
                raise Exception(
                    "Error: function_response (function_result.parts[0].function_response) is empty!"
                )
            if (
                not function_call_result.parts[0].function_response.response
                or function_call_result.parts[0].function_response.response is None
            ):
                raise Exception(
                    "Error: response (function_result.parts[0].function_response.response) is empty!"
                )
            function_results.append(function_call_result.parts[0])
            if cli_args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
