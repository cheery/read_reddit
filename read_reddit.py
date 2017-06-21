from datetime import datetime
from hackernews import HackerNews
from urlparse import urlparse
import praw, json

config_path = 'config.json'

with open('config.json', 'r') as fd:
    config = json.load(fd)

reddit = praw.Reddit(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    user_agent='linux:org.boxbase.read_reddit:v0.0.0 (by /u/htuhola)')

hn = HackerNews()

my_subreddits = config['my_subreddits']

# The list of sites that are shites.
blacklist = set([
    'codementor.io',        # blind leading deaf -websites
    'codewithoutrules.com', # stuff I am not interested about
    'orlandohamsho.com',
    'widgetsandshit.com'
])

all_submissions = []

print "Fetching reddit posts"
new_before = None
if 'before' not in config:
    for submission in mreddit.subreddit(my_subreddits).new(filter=1):
        old_before = submission.fullname
else:
    old_before = config['before']

    for submission in reddit.subreddit(my_subreddits).new(
            params={'before':old_before}):
        if new_before is None:
            new_before = submission.fullname
        if submission.domain in blacklist:
            continue
        submission_time = datetime.fromtimestamp(submission.created_utc)
        all_submissions.append((submission_time, 'reddit', submission))

if new_before == None:
    new_before = old_before
config['before'] = new_before

print "Fetching hacker news posts"
new_before = hn.get_max_item()
old_before = config.get('hn_before', new_before)
if new_before > old_before:
    for story_id in hn.new_stories(new_before - old_before):
        if story_id > new_before:
            new_before = story_id
        if story_id <= old_before:
            continue
        story = hn.get_item(story_id)
        if story.deleted:
            continue
        if story.url != None:
            domain = urlparse(story.url).netloc
            if domain in blacklist:
                continue
        submission_time = story.submission_time
        all_submissions.append((submission_time, 'hn', story))
config['hn_before'] = new_before

all_submissions.sort(key = lambda x: x[0])

for tstamp, which, submission in all_submissions:
    print '-' * 80
    if which == "reddit":
        if submission.url:
            print submission.url
        print u"\033[92m{}\033[0m [{}] {}".format(submission.subreddit, submission.score, submission.title)
    elif which == "hn":
        if submission.url:
            print submission.url
        print u"hacker news [{}] {}".format(submission.score, submission.title)
    else:
        print submission

with open('config.json', 'w') as fd:
    json.dump(config, fd, indent=4, sort_keys=True)
