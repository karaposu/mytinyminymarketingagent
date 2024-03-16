import json

system_message_dict={ "role": "system","content":
    "I am a post filterer designed to analyze forum posts based on provided post information and filter criteria. I evaluate whether a post is relevant to a specific product or content described in the filter information"
                      }

# Based on the product description and hookpoints, determine if this post is relevant and explain why.

# def get_post_filterer_gpt_user_message_dict(post, product_info):
#     # Constructs and returns a dictionary with the content dynamically created using manufacturer_name
#      return {
#         "role": "user",
#         "content": f"""Determine if the following post {post} is matching with my product/content in terms of definition, Benefits and Hookpoints.  Here is information about my product {product_info}. Use the structured format for your query to ensure the best possible accuracy and efficiency. Provide the results in a JSON result as 'is_relevant': '<value>', where value is the relevance of the post (either 1 or 0). If relavence is 1 please go head and craft an answer to this post using my product information and put the output in a  s information in a JSON as 'crafted_answer' <value> where value is the answer you crafted. if is_relevant is 0, return an empty crafted_answer"""
#     }

def get_post_filterer_gpt_user_message_dict(post, product_info):
    # Constructs and returns a dictionary with the content dynamically created using manufacturer_name
     return {
        "role": "user",
        "content": f""""I want you to analyse the the following post {post} and determine their relevance to my product. here is information about my product {product_info}. The function should return a JSON string containing two keys: 'is_relevant' and 'crafted_answer'. The 'is_relevant' key should have a value of 1 if the post matches my product in terms of definition, benefits, and hookpoints, and 0 otherwise. If 'is_relevant' is 1, the function should also generate a crafted answer using my product information and return it under the 'crafted_answer' key. If 'is_relevant' is 0, 'crafted_answer' should be an empty string."""  }


#
#  " {  "is_relevant": "1",  "crafted_answer": "<Here goes the crafted answer based on the product info>"
# }
# or
#
# {
#   "is_relevant": "0",
#   "crafted_answer": ""
# }
# Please ensure your response adheres to this structure."
#

