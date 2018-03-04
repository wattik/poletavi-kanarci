import praw
import passwords as pw
import pprint


def run():
    reddit = praw.Reddit(client_id=pw.client_id, client_secret=pw.client_secret,
                         password=pw.password, user_agent=pw.user_agent,
                         username=pw.username)

    submissions = reddit.subreddit("nba").hot(limit=10)
    for submission in submissions:
        pprint.pprint(submission.selftext_html)


if __name__ == '__main__':
    run()
