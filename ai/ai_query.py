import os
from openai import OpenAI
import json

# Replace 'your_openai_api_key' with your actual OpenAI API key


# manufacturer_name="enes"
# system_message_dict={
#                 "role": "system",
#                 "content": f"""
# "I am a lookup service designed to identify manufacturer names from strings provided to me. You can ask me to determine if a given string is a manufacturer's name, defined as any company or brand known for producing goods or products. Please provide the string in a structured format, and I will respond with information about the manufacturer, including a confidence level regarding the identification. Use the provided format for queries to ensure accurate and efficient processing."
#
#  """
# }

# user_message_dict={
#                 "role": "user",
#                 "content": f"""
#                    Determine if the following string {manufacturer_name} is a manufacturer's name or not.
#                 Use the structured format for your query to ensure the best possible accuracy and efficiency.
#                 Provide the results in a JSON result as 'result': '<value>',
#                 where value is the Full Name(without hypen) of the company you determined.
#                 If there is no likely choice, add it to the JSON result as 'result': 'None'
#                 If there are many choices nad you are confused whichone this string refers to, then provide this information in JSON
#                 result "flag": <value>  where value is a 1 if you are confused
#                 """
#             }
#
#
# m=[system_message_dict,user_message_dict ]
#

import ast
def query_chatgpt( gpt_type=None, messages=None, print_response=False  ):
    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
    gpt_type= "gpt-4-0125-preview"

    client=OpenAI()
    completion = client.chat.completions.create(model=gpt_type,
                                                messages= messages,
                                                response_format= {"type":"json_object"}, 
                                                seed=24,
               
               )
 
    content = completion.choices[0].message.content
    # if print_response:
    #   print("raw content:", content)

    content = content.strip('`')
    content = content.replace('\n', '')
    content = content.replace("json", '')

    # if print_response:
    #   print("stripped content:", content)
    
    try:
        # print(content)
        parsed = json.loads(content)
        # print("JSON is valid.")
    except json.JSONDecodeError:
        content_dict = ast.literal_eval(content)
        json_string = json.dumps(content_dict)
        parsed = json.loads(json_string) 
         
        
    # content = content.strip().strip('`').strip()
    # try:
    #     parsed_content = json.loads(content)
    #     return parsed_content
    # except json.JSONDecodeError as e:
    #     print(f"Error parsing JSON: {e}")
    # content = content.strip('`')
    # content = content.replace('\n', '')
    # content = content.replace("json", '')
    # # if print_response:
    # #   print(content)
    
    return parsed

