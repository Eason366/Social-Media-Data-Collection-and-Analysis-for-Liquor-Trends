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
    post_data = pd.DataFrame(columns=['id', 'Community', 'author', 'url', 'timestamp', 'text', 'upvote', 'upvote_ratio'])
    comment_data = pd.DataFrame(columns=['id', 'Community', 'author', 'url', 'timestamp', 'body', 'upvote'])
    for subreddit in subreddits:

        try:
            # get Posts
            posts = reddit.subreddit(subreddit)
            for submission in posts.top(limit=Post_limit):
                new_row = pd.DataFrame({
                    'id': [submission.id],  # ID of the submission.
                    'Community': [subreddit], # # subreddit
                    'author': [''] if submission.author is None else [submission.author.name],  # name of author
                    'url': ['https://www.reddit.com' + submission.permalink],  # A permalink for the submission.
                    'timestamp': [submission.created_utc],  # Time the submission was created, represented in `Unix Time`_.
                    'text': [submission.selftext],  # The submissions' selftext - an empty string if a link post.
                    'upvote': [submission.score],  # The number of upvotes for the submission.
                    'upvote_ratio': [submission.upvote_ratio]  # The percentage of upvotes from all votes on the submission.
                })
                post_data = pd.concat([post_data, new_row], ignore_index=True)

            # get comments
            i = 0
            for comment in reddit.subreddit(subreddit).stream.comments():
                if i >= comment_limit:
                    break
                new_row = pd.DataFrame({
                    'id': [comment.id],  # The ID of the comment.
                    'Community': [subreddit],  # subreddit
                    'author': [''] if comment.author is None else [comment.author.name],  # name of author
                    'url': ['https://www.reddit.com' + comment.permalink],  # A permalink for the comment.
                    'timestamp': [comment.created_utc],  # Time the comment was created, represented in `Unix Time`_.
                    'body': [comment.body],  # The body of the comment, as Markdown.
                    'upvote': [comment.score]  # The number of upvotes for the comment.
                })
                comment_data = pd.concat([comment_data, new_row], ignore_index=True)
                i += 1
        except Exception as e:
            print(f'{subreddit} is not available')

    post_data.to_csv(f'data/Reddit_Post_Data_{time.time()}.csv', encoding='utf_8_sig')
    comment_data.to_csv(f'data/Reddit_Comment_Data_{time.time()}.csv', encoding='utf_8_sig')


get_data()
