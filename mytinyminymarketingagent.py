
from post_exporter.reddit.praw_post_exporter import fetch_posts
from utils.LLM  import gpt, read_and_prepare_prompt
from tqdm import tqdm
from notificator.notificator import Notificator

class Mytinyminymarketingagent:
    def __init__(self, productinfo_yaml_path):
         self.productinfo_yaml_path= productinfo_yaml_path
         self.product_info = read_and_prepare_prompt(productinfo_yaml_path)
         self.notificator=Notificator()
         self.reddit_subreddit=None


    def set_reddit_settings(self, subreddit, post_order_cat, limit, export_comments=False):
        self.reddit_subreddit= subreddit
        self.reddit_post_order_cat = post_order_cat
        self.reddit_limit = limit
        self.reddit_export_comments = export_comments


    def scan(self):
        # self.reddit_scan( self.reddit_subreddit,
        #                   self.reddit_post_order_cat,
        #                   self.reddit_limit,
        #                   self.reddit_export_comments
        #                   )
        self.reddit_scan()
    def reddit_scan(self):
        if not self.reddit_subreddit:
            return 0

        subreddit= self.reddit_subreddit
        post_order_cat=    self.reddit_post_order_cat
        limit=  self.reddit_limit
        export_comments=self.reddit_export_comments

        posts, was_successful = fetch_posts(subreddit, limit, False)


        relevant_posts = []
        # for post in posts:
        for post in tqdm(posts, desc="Processing posts"):
            p = post['Text']
            link = post['Link']
            id = post['Post ID']

            is_relevant, crafted_answer = gpt(p, self.product_info, type="marketing", last_link=False)
            # print(is_relevant)
            if is_relevant == 1:
                relevant_posts.append({"id": id, "link": link, "post": post, "crafted_answer": crafted_answer})

        self.reddit_relevant_posts=relevant_posts
        return relevant_posts

    def notify(self):
        self.notificator.configure_telegram()
        for i in range(len(self.reddit_relevant_posts)):
            link= self.reddit_relevant_posts[i]["link"]
            crafted_answer= self.reddit_relevant_posts[i]["crafted_answer"]

            result = self.notificator.send_telegram_message(link)
            result = self.notificator.send_telegram_message(crafted_answer)

