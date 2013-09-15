from RedditBotClass import RedditBot
from DataAccess import DataAccessor
import praw
from datetime import datetime

dAccessor = DataAccessor()
rBot = RedditBot()
r = praw.Reddit(user_agent='MyFirstBot 1.0 by ItsSpelledFavreBot')
subredditname = 'greenbaypackers'

subreddit = r.get_subreddit(subredditname)

submissions = subreddit.get_hot(limit=10)

submission_set = []
prev_submission_ids = dAccessor.Get_Previous_Submission_IDs()

for submission in submissions:
    if len(prev_submission_ids) == 0 or prev_submission_ids[0].count(submission.id) == 0:
        post_date = datetime.fromtimestamp(submission.created).strftime('%Y-%m-%d %H:%M:%S')
        dict = {'SubmissionID': unicode(submission.id), 
                'SubmissionTitle': unicode(submission.title),
                'Subreddit': unicode(subredditname),
                'SubmissionScore': unicode(submission.score),
                'PostDate':post_date}
        submission_set.append(dict)

if len(submission_set) > 0:
    result = dAccessor.Insert_Submissions(submission_set)

#How do I do string formatting?
print 'Inserted {0} records'.format(str(len(submission_set)))

raw_input('hi')





