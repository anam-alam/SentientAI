import os,sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt
from call_function import available_functions,call_function





def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    #print("SentientAI: ")
    args = sys.argv[1:]
    user_prompt = " ".join(args)
    #print(system_prompt)
    
    if not args:
        print("Prompt not provided")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
    verbose = "--verbose" in args
    if verbose:
        args.remove("--verbose")
        
    user_prompt = " ".join(args)
    print(f"User prompt: {user_prompt}\n")


    generate_content(client, messages, verbose)



def generate_content(client, messages, verbose):
    response = client.models.generate_content(model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
            ),
    )
    if verbose:  
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # print("Response:")
    # print(response.text)
    for part in response.candidates[0].content.parts:
        if part.function_call:
            fn_result = call_function(part.function_call, verbose=verbose)
            fr = fn_result.parts[0].function_response
            if not fr or not fr.response:
                raise RuntimeError("No function response returned")

            
            if verbose:
                print(f"-> {fr.response}")
            
            # Print the actual result for tests
            if isinstance(fr.response, dict) and "result" in fr.response:
                print(fr.response["result"])
            elif isinstance(fr.response, dict) and "error" in fr.response:
                print(fr.response["error"])
            else:
                print(fr.response)

            return
            

    if not response.function_calls:
        print(response.text)
    else:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
           
        


if __name__ == "__main__":
    main()
