import praw
import os
from tqdm import tqdm  # Import tqdm
# Initialize PRAW with your client credentials
client_id = os.environ.get('REDDIT_CLIENT_ID')
client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
username = os.environ.get('REDDIT_USERNAME')
password = os.environ.get('REDDIT_PASSWORD')
user_agent="YourBot/0.1"

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def fetch_posts(subreddit_names, limit=10, export_comments=False, headers=None):
    aggregated_posts_data = []
    success = True  # Assume success unless an exception occurs
    if isinstance(subreddit_names, str):
        subreddit_names=[subreddit_names]

    #for subreddit_name in subreddit_names:  # Iterate over each subreddit name provided
    for subreddit_name in tqdm(subreddit_names, desc="Subreddit Post Fetching Progress"):
        posts_data = []
        try:
            subreddit = reddit.subreddit(subreddit_name)  # Access the subreddit
            #for submission in subreddit.new(limit=limit):
            for submission in tqdm(subreddit.new(limit=limit), desc=f"Fetching from {subreddit_name}", leave=False):
                post_data = {
                    "Subreddit": subreddit_name,  # Include subreddit name in post data
                    "Post ID": submission.id,
                    "Title": submission.title,
                    "Text": submission.selftext,  # Text content of the post
                    "Link": submission.url  # Direct URL to the post
                }
                # Optionally add comments if export_comments is True
                if export_comments:
                    post_data["Comments"] = []
                    submission.comments.replace_more(limit=0)  # Load all comments; be cautious with large threads
                    for comment in submission.comments.list():
                        post_data["Comments"].append({
                            "Comment ID": comment.id,
                            "Text": comment.body
                        })
                posts_data.append(post_data)
            aggregated_posts_data.extend(posts_data)  # Add the posts from the current subreddit to the aggregate list
        except Exception as e:
            print(f"An error occurred while fetching posts from {subreddit_name}: {e}")
            success = False  # Set success to False if any exception occurs

    return aggregated_posts_data, success



