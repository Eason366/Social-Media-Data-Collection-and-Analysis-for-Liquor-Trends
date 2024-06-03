import praw
import sys
import warnings

sys.path.append("..")
import tool

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

Post_limit = 50  # number of posts for each Reddit Communities

posts_data = []


def get_data():
    for subreddit in subreddits:
        print(f'Get Data from {subreddit}.......')
        try:
            # get Posts
            posts = reddit.subreddit(subreddit)
            for submission in posts.hot(limit=Post_limit):
                post_info = {
                    'id': submission.id,  # ID of the submission.
                    'Community': subreddit,  # # subreddit
                    'author': '' if submission.author is None else submission.author.name,  # name of author
                    'url': 'https://www.reddit.com' + submission.permalink,  # A permalink for the submission.
                    'timestamp': submission.created_utc,
                    # Time the submission was created, represented in `Unix Time`_.
                    'text': submission.selftext,  # The submissions' selftext - an empty string if a link post.
                    'upvote': submission.score,  # The number of upvotes for the submission.
                    'upvote_ratio': submission.upvote_ratio,
                    # The percentage of upvotes from all votes on the submission.
                    'comments': []
                }

                # Collect comments for the post
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    comment_info = {
                        'comment_id': comment.id,
                        'comment_body': comment.body,
                        'comment_score': comment.score,
                        'comment_created': comment.created
                    }
                    post_info['comments'].append(comment_info)

                posts_data.append(post_info)

        except Exception as e:
            print(f'{subreddit} is not available')

    return posts_data


Datas = get_data()
connect = tool.connect_NoSQL('Reddit')
tool.insert_data(connect, Datas)