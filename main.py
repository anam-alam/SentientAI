import os,sys,time
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITERS
from call_function import available_functions,call_function
from prompts import system_prompt



def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    args = sys.argv[1:]
    verbose = "--verbose" in args

    if verbose:
        args.remove("--verbose")
        
    user_prompt = " ".join(args)
    print(f"User prompt: {user_prompt}\n")
    
    if not args:
        print("Prompt not provided")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
    
    
    i = 0
    while True:
        i += 1
        if i > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            #time.sleep(4)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            error_str = str(e)
            print(f"Error in generate_content: {error_str}")

            if "RESOURCE_EXHAUSTED" in error_str:
                try:
                    # Extract retryDelay dynamically
                    error_obj = json.loads(error_str.split("{", 1)[1])
                    retry_delay = int(
                        error_obj['error']['details'][2]['retryDelay'].rstrip('s')
                    )
                    print(f"Quota exceeded. Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                except Exception:
                    #print(f"\n[DEBUG] Attempt {i}: Error in generate_content: {e}\n")
                    print("Failed to parse retryDelay. Defaulting to 20 seconds.")
                    time.sleep(20)
            else:
                raise e

    generate_content(client, messages, verbose)



def generate_content(client, messages, verbose):
    
    response = client.models.generate_content(model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
            ),
    )
    if verbose and response.usage_metadata:  
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # print("Response:")
    # print(response.text)
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            if function_call_content:
                messages.append(function_call_content)
    
    if not response.function_calls:
        return response.text
    
    function_responses: list[types.Part] = []
    for function_call_part in response.function_calls:
        result = call_function(function_call_part,verbose)
        #print(f"[DEBUG] Function call result: {result.parts[0].function_response.response}")
        if not result:
            raise Exception(f"no result from calling \"{function_call_part.name}\" with args \"{function_call_part.args}\"")

        if (
            not result.parts
            or not result.parts[0].function_response
        ):
            raise Exception("empty function call result")

        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
