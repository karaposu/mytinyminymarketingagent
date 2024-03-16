
from mytinyminymarketingagent import Mytinyminymarketingagent

tinyagent= Mytinyminymarketingagent()
# subreddit= "StableDiffusion"
subreddits=["StableDiffusion", "comfyui"]

post_order_cat= "new"
limit= 30
productinfo_yaml_path= "agent_comfyui.yaml"

relevant_posts=tinyagent.reddit_agent(subreddits, post_order_cat, limit, productinfo_yaml_path )

# print(len(relevant_posts))

for i in range(len(relevant_posts)):
    print(relevant_posts[i]["link"], relevant_posts[i]["crafted_answer"])



