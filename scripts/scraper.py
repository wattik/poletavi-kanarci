import praw
import passwords as pw
import pprint
from datetime import datetime


def run():
    reddit = praw.Reddit(client_id=pw.client_id, client_secret=pw.client_secret,
                         password=pw.password, user_agent=pw.user_agent,
                         username=pw.username)

    submissions = reddit.subreddit("nba").new(limit=2)

    for submission in submissions:
        created = datetime.fromtimestamp(int(submission.created_utc))
        permalink = submission.permalink
        name = submission.name
        subreddit_name = submission.subreddit_name_prefixed
        title = submission.title
        text_html = submission.selftext_html
        text = submission.selftext

        print("created: " + str(created))
        print("permalink: " + permalink)
        print("name: " + name)
        print("subreddit: " + subreddit_name)
        print("title: " + title)
        print("text: " + text)


if __name__ == '__main__':
    run()
