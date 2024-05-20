import praw
import pandas as pd
import time
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
# a script-type OAuth application
# Instantiate an instance of PRAW
reddit = praw.Reddit(
    user_agent="BOOZEVILLA by u/Eason_366",
    client_id="RpEPKBvUAzTR-W8oNrrVMQ",
    client_secret="GJzruoXTpzt33vuCMEeDqpop3YiI9w"
)
# Reddit Communities List
subreddits = ['beer', 'cocktails', 'whiskey', 'wine', 'scotch', 'trquila', 'rum', 'gin', 'homebrewing',
              'BarBattlestations', 'stopdrinking', 'drunk', 'liquor', 'vodta', 'brandy']

Post_limit = 1  # number of posts for each Reddit Communities
comment_limit = 1  # number of comment_ for each Reddit Communities


def get_data():
    post_data = pd.DataFrame(columns=['id', 'Community', 'author', 'url', 'timestamp', 'text'])
    comment_data = pd.DataFrame(columns=['id', 'Community', 'author', 'url', 'timestamp', 'body'])
    for subreddit in subreddits:

        try:
            # get Posts
            posts = reddit.subreddit(subreddit)
            for submission in posts.top(limit=Post_limit):
                new_row = pd.DataFrame({
                    'id': [submission.id],
                    'Community': [subreddit],
                    'author': [''] if submission.author is None else [submission.author.name],
                    'url': ['https://www.reddit.com' + submission.permalink],
                    'timestamp': [submission.created_utc],
                    'text': [submission.selftext]
                })
                post_data = pd.concat([post_data, new_row], ignore_index=True)

            # get comments
            i = 0
            for comment in reddit.subreddit(subreddit).stream.comments():
                if i >= comment_limit:
                    break
                new_row = pd.DataFrame({
                    'id': [comment.id],
                    'Community': [subreddit],
                    'author': [''] if comment.author is None else [comment.author.name],
                    'url': ['https://www.reddit.com' + comment.permalink],
                    'timestamp': [comment.created_utc],
                    'body': [comment.body]
                })
                comment_data = pd.concat([comment_data, new_row], ignore_index=True)
                i += 1
        except Exception as e:
            print(f'{subreddit} is not available')

    post_data.to_csv(f'data/Reddit_Post_Data_{time.time()}.csv', encoding='utf_8_sig')
    comment_data.to_csv(f'data/Reddit_Comment_Data_{time.time()}.csv', encoding='utf_8_sig')


get_data()
