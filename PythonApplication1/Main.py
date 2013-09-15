from RedditBotClass import RedditBot
rBot = RedditBot('greenbaypackers')
last_submissions = rBot.Get_Submissions_Since_Last_Post()
rBot.Insert_Submissions(last_submissions)
