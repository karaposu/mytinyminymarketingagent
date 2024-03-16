import requests
import os
from  datetime import datetime
import json
import argparse


CATEGORY_ID = ["new", "top", "controversial", "hot", "rising"]
def get_reddit_token(client_id, client_secret):
    """
    Authenticate with Reddit to get an access token.
    """
    client_id = os.environ.get('REDDIT_CLIENT_ID')
    client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
    username = os.environ.get('REDDIT_USERNAME')
    password = os.environ.get('REDDIT_PASSWORD')

    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {'grant_type': 'password',
            'username': username,
            'password': password}
    headers = {'User-Agent': 'YourBot/0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    token = res.json()['access_token']
    return token


def subreddit_valid(subreddit, access_token):
    """
    Check if a subreddit is valid using the authenticated Reddit API.
    """
    headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": "YourBot/0.1"
    }
    url = f"https://oauth.reddit.com/r/{subreddit}/about"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', {}).get('subscribers', -1) >= 0 and data.get('data', {}).get('subreddit_type',
                                                                                             '') != 'private'
    return False


def rpe_request(method, url, headers=None, **kwargs):
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-GB,en;q=0.9",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1"
        }
    return requests.Request(method, url, headers=headers, **kwargs).prepare()

def fetch_posts(subreddit, category_id, limit, export_comments, headers):
    """
    Fetch posts from a subreddit and optionally export comments.
    """

    client_id = 'OFeP82ya8RXZ-Fg2Q6SYpQ'
    client_secret = 'oIUoQnaRDSDlFT1nJKPNLvnssNbxCw'
    access_token = get_reddit_token(client_id, client_secret)
    subreddit = subreddit

    headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": "YourBot/0.1"
    }

    url = f"https://oauth.reddit.com/r/{subreddit}/{CATEGORY_ID[category_id]}.json?limit={limit}"
   # url = f"https://www.reddit.com/r/{subreddit}/{CATEGORY_ID[category_id]}.json?limit={limit}"
    req = rpe_request('GET', url, headers=headers)
    with requests.Session() as session:
        resp = session.send(req)
    if resp.status_code == 200:
        print("success")
        data = resp.json()
        print("data", data)
        posts = [child['data'] for child in data['data']['children']]
        gathered_posts=gather_posts(posts, subreddit, category_id, export_comments)
    else:
        print(f"HTTP request failed with status code {resp.status_code}")

    return gathered_posts


def gather_posts(posts, subreddit, category_id, export_comments):
    """
    Export posts to JSON files and optionally fetch and export comments.
    """
    now = datetime.now()
    base_path = os.path.join(subreddit, now.strftime("%d-%b-%Y"), now.strftime("%H-%M-%S"), CATEGORY_ID[category_id])
    os.makedirs(base_path, exist_ok=True)

    collected_posts = []
    for i, post in enumerate(posts):
        # If exporting comments, fetch and append them
        if export_comments:
            # Assume fetch_comments function now returns comments instead of saving them
            comments = fetch_comments(post['permalink'])
            # Append comments to the post dictionary before appending it to the list
            post['comments'] = comments

        # Append the post, now possibly with comments, directly to the list
        collected_posts.append(post)
        print(f"Post {i + 1} added to the list with its comments.")

    extracted_posts = []
    for post in collected_posts:
        print(post)
        extracted_posts.append({
            'id': post.id,
            'title': post.title,
            'selftext': post.selftext,
            'url': post.url,
            'created_utc': post.created_utc,
            'permalink': post.permalink,
        })
    return  extracted_posts



def export_posts(posts, subreddit, category_id, export_comments):
    """
    Export posts to JSON files and optionally fetch and export comments.
    """
    now = datetime.now()
    base_path = os.path.join(subreddit, now.strftime("%d-%b-%Y"), now.strftime("%H-%M-%S"), CATEGORY_ID[category_id])
    os.makedirs(base_path, exist_ok=True)

    for i, post in enumerate(posts):
        filename = os.path.join(base_path, f"post-{post['id']}.json")
        with open(filename, 'w') as f:
            json.dump(post, f, indent=2)
        print(f"Saved post {i + 1} to path {filename}")

        if export_comments:
            fetch_comments(post['permalink'], base_path, i)


def fetch_comments(permalink, path, post_index):
    """
    Fetch comments for a post and save them.
    """
    comments_url = f"https://www.reddit.com{permalink}.json"
    req = rpe_request('GET', comments_url)
    with requests.Session() as session:
        resp = session.send(req)
    if resp.status_code == 200:
        data = resp.json()
        if len(data) > 1 and 'data' in data[1] and 'children' in data[1]['data']:
            comments = [child['data'] for child in data[1]['data']['children']]
            export_comments(comments, path, post_index)
    else:
        print(f"Failed to fetch comments for post index {post_index}")


def export_comments(comments, path, post_index):
    """
    Export comments to JSON files.
    """
    comments_path = os.path.join(path, "comments")
    os.makedirs(comments_path, exist_ok=True)
    for i, comment in enumerate(comments):
        filename = os.path.join(comments_path, f"comment-{i + 1}.json")
        with open(filename, 'w') as f:
            json.dump(comment, f, indent=2)
        print(f"Saved comment {i + 1} for post {post_index + 1} to path {filename}")

# Use your actual Reddit credentials here
client_id = 'OFeP82ya8RXZ-Fg2Q6SYpQ'
client_secret = 'oIUoQnaRDSDlFT1nJKPNLvnssNbxCw'
access_token = get_reddit_token(client_id, client_secret)

# Example usage
subreddit = 'golang'
is_valid = subreddit_valid(subreddit, access_token)


headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-GB,en;q=0.9",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1"
        }


headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": "YourBot/0.1"
    }

print(f"Is '{subreddit}' a valid subreddit? {is_valid}")


def get_reddit_user_info(access_token):
    """
    Fetch information about the authenticated Reddit user.
    """
    headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": "YourBot/0.1"
    }
    response = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    if response.status_code == 200:
        return response.json()  # This is the user's information
    else:
        return f"Failed to fetch user info. Status code: {response.status_code}"


# Use the access token you've obtained
access_token = get_reddit_token(client_id, client_secret)

# Fetch and print the Reddit user information
user_info = get_reddit_user_info(access_token)
# print(user_info)

# fetch_posts(subreddit, category_id, limit, export_comments)
fetch_posts(subreddit, 0, 5, False, headers=headers)

# posts = []
# for post in subreddit.new(limit=limit):
#     posts.append({
#         'id': post.id,
#         'title': post.title,
#         'selftext': post.selftext,
#         'url': post.url,
#         'created_utc': post.created_utc,
#         'permalink': post.permalink,
#     })
#
# return posts