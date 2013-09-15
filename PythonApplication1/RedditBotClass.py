import praw
from os import open
from DataAccess import DataAccessor
from ConfigParser import ConfigParser
from datetime import datetime

config = ConfigParser()
config.read('appconfig.cfg')
useragent_value = config.get('RedditConfig','useragent_string')
username_value = config.get('RedditConfig', 'username_string',1)
pwd_value = config.get('RedditConfig','pwd_string',1)

class RedditBot:
    """initializer for accessing reddit, querying posts, etc."""

    def __init__(self, init_subreddit=None):
        
        self.r = praw.Reddit(user_agent=useragent_value)
        self.r.login(username_value, pwd_value)#config?
        self.subreddit = None
        self.dAccessor = DataAccessor()

        if init_subreddit is not None:
            #self.subreddit = self.Set_Subreddit(init_subreddit)
            self.subreddit = self.r.get_subreddit(init_subreddit)

    '''Set the subreddit of the RedditBot instance.\r\n\r\nAccepts
     string of subreddit to set'''
    def Set_Subreddit(self, subreddit_name):
        try:
            #theres gotta be a better way of doing this. maybe a ping?
            comments = self.r.get_subreddit(subreddit_name).get_hot(limit=1)
            for c in comments:
                x = c.title
        except:
            print 'subreddit!'
            return
        self.subreddit = self.r.get_subreddit(subreddit_name)
        #how do I check to make sure this is a valid subreddit?
    
    '''Gets x number of top posts for a given subreddit.\r\n\r\n\Accepts 
    integer of number of top posts to query'''
    def Get_Hot(self, number_of_posts):
        if(self.subreddit):
            return self.subreddit.get_hot(limit=number_of_posts)

    #not working. reddit returns posts that are older than created date of id passed in
    def Get_Submissions_Since_Last_Post(self):
        if(self.subreddit):
            last_id = self.Get_Last_Comment_ID()
            return self.subreddit.get_top(limit=None, 
                                          place_holder=last_id)

    def Get_Last_Comment_ID(self):
        ids = self.dAccessor.Get_Previous_Submission_IDs()
        id = ids[0][0]
        return id

    def Insert_Submissions(self, submissions):
        prev_submission_ids = self.dAccessor.Get_Previous_Submission_IDs()
        submission_set = []

        for submission in submissions:
            if(self.subreddit):
                if prev_submission_ids[0].count(submission.id) == 0:
                    post_date = datetime.fromtimestamp(submission.created).strftime('%Y-%m-%d %H:%M:%S')
                    dict = {'SubmissionID': unicode(submission.id), 
                            'SubmissionTitle': unicode(submission.title),
                            'Subreddit': unicode(self.subreddit),
                            'SubmissionScore': unicode(submission.score),
                            'PostDate':post_date}
                    submission_set.append(dict)

        self.dAccessor.Insert_Submissions(submission_set)