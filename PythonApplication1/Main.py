from RedditBotClass import RedditBot
from praw import helpers, errors, objects

rBot = RedditBot('greenbaypackers')
submissions = rBot.Get_Submissions_Since_Last_Post()
already_submitted_ids = rBot.dAccessor.Get_Previous_Submission_IDs()

insert_set = []

for s in submissions:
    s.replace_more_comments(limit=10, threshold=3)
    flat_comments = helpers.flatten_tree(s.comments)

    print s.title
    for c in flat_comments:
        if not isinstance(c, objects.MoreComments) and 'rogers' in c.body.lower() and c.id not in already_submitted_ids:
            try:
                c.reply('Its spelled Rodgers')
                print 'Replied to comment {0} by user {1}'.format(c.body.lower(), c.author)
                insert_set.append(c)
            except errors.RateLimitExceeded, e:
                print e.message
            except BaseException, e:
                print e.message

rBot.Insert_Submissions(insert_set)

raw_input('hit button to continue')