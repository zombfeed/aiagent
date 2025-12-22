import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    ''' prompt ai
        client: genai client
        prompts: [] list of messages to prompt with
    '''
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompts)
    if not response:
        raise RuntimeError("failed API request")
    metadata = response.usage_metadata
    return response, metadata

def main():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    cli_args = parse_args()

    user_prompt = cli_args.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    response, metadata = prompt_ai(client, messages)
    
    if cli_args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {metadata.prompt_token_count}\nResponse tokens: {metadata.candidates_token_count}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
