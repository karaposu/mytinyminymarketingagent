
from mytinyminymarketingagent import Mytinyminymarketingagent


productinfo_yaml_path= "agent_comfyui.yaml"
agent= Mytinyminymarketingagent(productinfo_yaml_path)

# subreddit= "StableDiffusion"
subreddits=["StableDiffusion", "comfyui"]
post_order_cat= "new"
limit= 30


agent.set_reddit_settings(subreddits, post_order_cat, limit,export_comments=False )
relevant_posts=agent.reddit_scan()
agent.notify()

# print(len(relevant_posts))

for i in range(len(relevant_posts)):
    print(relevant_posts[i]["link"], relevant_posts[i]["crafted_answer"])



