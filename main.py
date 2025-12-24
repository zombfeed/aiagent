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
    iterations = 0
    available_functions = call_functions.available_functions
    while iterations <= 20:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompts,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
            if not response:
                raise RuntimeError("Error: failed API request")
            for candidates in response.candidates:
                prompts.append(candidates.content)
            if response.function_calls:
                for function_call in response.function_calls:
                    function_call_result = call_functions.call_functions(function_call)
                    if not function_call_result.parts:
                        raise Exception(
                            "Error: parts (function_result.parts) is empty!"
                        )
                    if not function_call_result.parts[0].function_response:
                        raise Exception(
                            "Error: function_response (function_result.parts[0].function_response) is empty!"
                        )
                    if (
                        not function_call_result.parts[0].function_response.response
                        or function_call_result.parts[0].function_response.response
                        is None
                    ):
                        raise Exception(
                            "Error: response (function_result.parts[0].function_response.response) is empty!"
                        )
                    prompts.append(
                        types.Content(
                            role="user",
                            parts=[function_call_result.parts[0]],
                        )
                    )

            if not response.function_calls and response:
                return response
        except Exception as e:
            print(f"Error: {e}")
            return None
    return None


def main():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    cli_args = parse_args()

    user_prompt = cli_args.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    response = prompt_ai(client, messages)
    if not response:
        raise Exception("Error: response not found")
    if cli_args.verbose:
        print(f"User prompt: {user_prompt}")
        print(
            f"Prompt tokens: {response.metadata.prompt_token_count}\nResponse tokens: {response.metadata.candidates_token_count}"
        )

    print(f"Final Response:\n{response.text}")


if __name__ == "__main__":
    main()
