
from post_exporter.reddit.praw_post_exporter import fetch_posts
from utils.LLM  import gpt, read_and_prepare_prompt
from tqdm import tqdm

class Mytinyminymarketingagent:
    def __init__(self):
         pass
    def reddit_agent(self,subreddit, post_order_cat, limit, productinfo_yaml_path ):
        posts, was_successful = fetch_posts(subreddit, limit, False)

        product_info = read_and_prepare_prompt(productinfo_yaml_path)
        relevant_posts = []
        # for post in posts:
        for post in tqdm(posts, desc="Processing posts"):
            p = post['Text']
            link = post['Link']
            id = post['Post ID']

            is_relevant, crafted_answer = gpt(p, product_info, type="marketing", last_link=False)
            # print(is_relevant)
            if is_relevant == 1:
                relevant_posts.append({"id": id, "link": link, "post": post, "crafted_answer": crafted_answer})

        return relevant_posts

