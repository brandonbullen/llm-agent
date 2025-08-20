import argparse
import os
import sys

from google import genai
from google.genai import types
from dotenv import load_dotenv


parser = argparse.ArgumentParser(
    prog='AI Code Assistant',
    description='Takes prompts and passes them to an LLM.'
)

parser.add_argument('user_prompt')
parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()


def main():
    load_dotenv()


    if not args.user_prompt:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Maybe we keep this for later?
    # user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]

    generate_content(client, messages)  
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")



def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    print("Response:")
    print(response.text)
    
    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
