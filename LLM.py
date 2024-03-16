import yaml
import time
import pandas as pd
import os
from openai import OpenAI
import json
# from tqdm import tqdm
from typing import Union
import os
os.environ['OPENAI_API_KEY'] = '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'
from ai.ai_query import query_chatgpt


pd.options.mode.chained_assignment = None
import logging


from gpt_definitions import get_post_filterer_gpt_user_message_dict
from gpt_definitions import system_message_dict



def read_and_prepare_prompt(yaml_file_path):

    # Reading and parsing the YAML file
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)

    # Accessing the parsed content
    product_description = config['productDescription']
    hookpoints = config['hookpoints']
   # print("hookpoints",hookpoints)
    # Constructing the prompt
    def construct_prompt(product_description, hookpoints):
        prompt = f"Product Name: {product_description['name']}\n"
        prompt += f"Description: {product_description['description']}\n"
        prompt += f"Target Audience: {product_description['targetAudience']}\n"
        prompt += "Benefits:\n"
        for benefit in product_description['benefits']:
            prompt += f"- {benefit}\n"
        prompt += "\nHookpoints:\n"
        for hookpoint in hookpoints:
            prompt += f"- {hookpoint['description']}\n"
        return prompt

    # Constructing the prompt using the parsed data
    prompt = construct_prompt(product_description, hookpoints)

    # Returning the constructed prompt
    return prompt




def gpt_based_manuf_normalizer_for_1_value( gpt_type=None, messages=None):
    successfully_normalized = 0

    response = query_chatgpt( gpt_type=gpt_type, messages=messages, print_response=True)
    # print("" )
    # print("")
    # print(response)
    # print("")
    is_relevant = response['is_relevant']
    crafted_answer = response['crafted_answer']

    return is_relevant, crafted_answer


def gpt(post, product_info, type="marketing", last_link=False):
        succesfully_normalized=0
        if type == "marketing":
            messages = [system_message_dict, get_post_filterer_gpt_user_message_dict(post,product_info)]
            file_path = "full_gpt_request.txt"
            with open(file_path, 'w') as file:
                file.write( str(messages[1]))  # Writing the text to the file
        # elif type == "full_name_finder":
        #     messages = [system_message_dict, get_fullname_finder_gpt_user_message_dict(self.value)]
        # elif type == "normalizer":

        gpt_type = "gpt-4-0125-preview"

        if not succesfully_normalized:
            pass

        is_relavent, crafted_answer = gpt_based_manuf_normalizer_for_1_value(gpt_type=gpt_type, messages=messages)
            # print(f" -> gpt-{type}                [{self.value}>>> {normalized_value}]")
        return [is_relavent,crafted_answer]
            # if is_relavent:
            #     print('\u2713')
            #     # self.gpt_normalized = normalized_value
            #     # self.value = normalized_value
            #     # # r=self.regex().regex_normalized
            #     # r = self.regex(separate=True).regex_normalized
            #     # self.normalized = r
            #     succesfully_normalized = True





# Example usage (Note: This will not execute here since we can't access file systems directly):
# yaml_file_path = 'path/to/your/config.yaml'
# prompt = read_and_prepare_prompt(yaml_file_path)
# print(prompt)

# This is a template of how you could structure the function in your Python environment.
# You would need to replace 'path/to/your/config.yaml' with the actual path to your YAML configuration file.
