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

def parse_user_prompt():
    parser = argparse.ArgumentParser(description="AI Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    args = parser.parse_args()
    return args.user_prompt

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
    
    userprompt = parse_user_prompt()
    messages = [types.Content(role="user", parts=[types.Part(text=userprompt)])]
    response, metadata = prompt_ai(client, messages)
    
    print(f"User prompt: {userprompt}")
    print(f"Prompt tokens: {metadata.prompt_token_count}\nResponse tokens: {metadata.candidates_token_count}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
