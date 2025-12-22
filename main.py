import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API Key not found")

    client = genai.Client(api_key=api_key)

    print(client.models.generate_content(model="gemini-2.5-flash", 
                                         contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
          .text)

if __name__ == "__main__":
    main()
