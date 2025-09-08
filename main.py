import os,sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt





def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    print("SentientAI: ")
    args = sys.argv[1:]
    user_prompt = " ".join(args)
    #print(user_prompt)
    
    if not args:
        print("Prompt not provided")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    verbose = "--verbose" in sys.argv
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
    if verbose:
        print(f"User prompt: {user_prompt}\n")
        
    generate_content(client, messages, verbose)



def generate_content(client, messages, verbose):
    response = client.models.generate_content(model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt))
    if verbose:  
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print("Response:")
    print(response.text)
        


if __name__ == "__main__":
    main()
