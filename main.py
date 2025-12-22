import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API Key not found")

    client = genai.Client(api_key=api_key)
    userprompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    response = client.models.generate_content(model="gemini-2.5-flash", contents=userprompt)
    metadata = response.usage_metadata
    if not response:
        raise RuntimeError("failed API request")
    print(f"User prompt:{userprompt}")
    print(f"Prompt tokens: {metadata.prompt_token_count}\nResponse tokens: {metadata.candidates_token_count}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
