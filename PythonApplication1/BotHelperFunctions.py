import praw

def Listize_DB_Result(db_result):
    """transform DB result into list"""
    list_result = []
    try:
        num_of_table_columns = len(db_result[0])
        i = 0
    
        while i < num_of_table_columns:
            sub_list = []
            for r in db_result:
                sub_list.append(r[i])
            list_result.append(sub_list)
            i += 1
        return list_result
    except:
        return list_result


def CommentChecker(reddit_posts, search_string):
    '''iterates through comments of each reddit_post, returns post that contains search_string)'''
    list_of_posts = []
    for post in reddit_posts:
        praw.helpers.flatten_tree(post.comments)
        for comment in post.comments:
            if comment.count(search_string) > 0:
                list_of_posts.append(post)
                return
    return list_of_posts