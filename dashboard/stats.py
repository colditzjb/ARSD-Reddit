
from calendar import c
from datetime import datetime, timedelta
import numpy as np
import json 
import time
#in case we want to catch this error (happened to me once for no reason)
# from prawcore.exceptions import Forbidden
# import nltk
# import pprint

subsDict = {}
with open('dashboard/subreddits.txt') as myfile:
    for line in myfile:
        name, description = line.partition("=")[::2]
        subsDict[name.strip()] = description.strip()
supportSubs = list(subsDict.keys())
for i in range(len(supportSubs)):
    supportSubs[i] = supportSubs[i][2:]

def activityStats(submissions, comments, upvotedSubmissions, downvotedSubmissions):
    timevec = []

    n = 0
    newday = 0

    for item in submissions:
        timeObj = item['created']
        day = int(timeObj/86400)
        c = timevec.count(day)
        if c == 0:
            timevec.append(day)
            newday += 1
        n+= 1
		
    for item in comments:
        timeObj = item['created']
        day = int(timeObj/86400)
        c = timevec.count(day)
        if c == 0:
            timevec.append(day)
            newday += 1
        n+= 1

    for item in upvotedSubmissions:
        timeObj = item['created']
        day = int(timeObj/86400)
        c = timevec.count(day)
        if c == 0:
            timevec.append(day)
            newday += 1
        n+= 1

    for item in downvotedSubmissions:
        timeObj = item['created']
        day = int(timeObj/86400)
        c = timevec.count(day)
        if c == 0:
            timevec.append(day)
            newday += 1
        n+= 1
        
	
    daysact = newday
    postact = n/newday
	
    return daysact, postact


def getAccountAge(user):
    date = datetime.fromtimestamp(user.created_utc)
    now = datetime.now()
    difference = now - date
    years = difference.days / 365
    # days = difference % 365

    return difference.days

def postingActivityDay(comments):
    supportSubs = ['test', 'videos','pcgaming']
    DoTW = {'Sun': 0, 'Mon': 0, 'Tues': 0, 'Wed': 0, 'Thur': 0, 'Fri': 0, 'Sat': 0,}
    for comment in comments:
        # if(str(comment.subreddit) in supportSubs):
        if datetime.fromtimestamp(comment['created']) > datetime.today() - timedelta(days=90):
            unix_val = datetime.fromtimestamp(comment['created'])
            day = unix_val.weekday()
            if(day == 0): day = 'Sun'
            elif(day == 1): day = 'Mon'
            elif(day == 2): day = 'Tues'
            elif(day == 3): day = 'Wed'
            elif(day == 4): day = 'Thur'
            elif(day == 5): day = 'Fri'
            elif(day == 6): day = 'Sat'
            if(day in DoTW):
                DoTW[day] += 1
    return DoTW

# returns two dictionaries in a list. One contains submission frequency,
# the other has comment frequency both sorted by subreddit
def activityCountSubreddit(comments, submissions):
    subListComments = {}
    subListSubmissions = {}
    for comment in comments:
        # if datetime.fromtimestamp(comment['created']) > datetime.today() - timedelta(days=90):
        if(str(comment['subreddit']) in subListComments):
            subListComments[str(comment['subreddit'])] += 1
        else:
            subListComments[str(comment['subreddit'])] = 1
    for submission in submissions:
        if(str(submission['subreddit']) in subListSubmissions):
            subListSubmissions[str(submission['subreddit'])] += 1
        else:
            subListSubmissions[str(submission['subreddit'])] = 1
    aList = []
    aList.append(subListComments)
    aList.append(subListSubmissions)
    return aList

def getMax(theDict):
    max_key = max(theDict, key=theDict.get)
    return max_key, theDict[max_key]

def wordsDict(comments, size):
    start = time.time()
    supportSubs = ['test', 'videos','pcgaming']
    wordsMain = {}
    for comment in comments:
        # if(str(comment.subreddit) in supportSubs):
            body = str(comment['body'])
            wordList = body.split()
            for word in wordList:
                word = word.lower()
                word = word.strip('.')
                for char in word:
                    if char in " ?.!/;:,":
                        word.replace(char,'')
                
                if word not in wordsMain:
                    wordsMain[word] = 1
                else:
                    wordsMain[word] += 1
    deleteList = []
    with open('dashboard/stopwords.txt') as file:
        contents = file.read()
        for key in wordsMain:
            if key in contents:
                deleteList.append(key)
        for word in deleteList:
            del wordsMain[word]
    # print(wordsMain)
    {k: v for k, v in wordsMain.items() if v}
    wordsMain = dict(sorted(wordsMain.items(), key=lambda item: item[1]))
    wordsMain = dict(list(wordsMain.items())[-size:])
    json_object = json.dumps(wordsMain, indent = 4) 
    # print(json_object)
    end = time.time()
    # print(f'wordsDict() runtime: {end - start}')
    return json_object

def averageCommentLengthSupport(comments):
    commentLengths = []
    supportSubs = ['test', 'videos','pcgaming']
    for comment in comments:
        # if(str(comment.subreddit) in supportSubs):
            body = str(comment['body'])
            if(len(body) > 5): #dont count comments less than 5 characters
                commentLengths.append(len(body))

    avg = np.average(commentLengths)
    median = np.median(commentLengths)
    limited_float = round(avg, 2)
    output = []
    output.append(limited_float) 
    output.append(median)
    return output

def getSupportSubs():
    
    return subsDict

def commentsOnDaysEngaged(comments):
    stats = []
    supportSubs = ['test', 'videos', 'pcgaming']
    commentDates = {}
    totalComments = 0
    for comment in comments:
        # if(str(comment['subreddit']) in supportSubs):
            
            unix_val = datetime.fromtimestamp(comment['created'])
            strippedDate = unix_val.date()
            if(strippedDate in commentDates):
                commentDates[strippedDate] += 1
                totalComments += 1
            else:
                commentDates[strippedDate] = 1
                totalComments += 1
    res = sum(commentDates.values()) / totalComments
    res = "{:.1f}".format(res)
    return res

def getBestComment(comments):
    max = comments[0]
    for comment in comments:
        if comment['score'] > max['score']:
            max = comment
    print(len(comment['body']))
    
    return max

def getWorstComment(comments):
    min = comments[0]
    for comment in comments:
        if comment['score'] < min['score']:
            min = comment
    return min

def weeklyComments(comments):
    return False #lol 

#should accept all three dictionaries with their respective frequencies organized by subreddit
def getMaxValues(comments, submissions, upvotes):
    
    return 0

def get_subreddit_stats(subreddit):
    '''
    Get stats for a subreddit.

    Keyword arguments:
    subreddit = an instance of Praw's subreddit class. 

    Returns a dictionary.
    
    '''
    sub_stats = {
        'title': subreddit.display_name,
        'description': subreddit.public_description,
        'subscriber_count': subreddit.subscribers
    }
    return sub_stats

def get_post_history(user):
    '''
    Get user's post history.

    Keyword arguments:
    user = an instance of Praw's redditor class.

    Returns a list of each post (as a dictionary).
    
    '''
    post_history = []
    for submission in user.submissions.new():
        temp = submission.subreddit
        post = {
            'id': submission.id,
            'title': submission.title,
            'created': submission.created_utc,
            'subreddit': temp.display_name,
            'body':submission.selftext,
            'num_comments': submission.num_comments
        } 
        post_history.append(post)
    return post_history

def get_posts_in_subreddit(post_history, subreddit):
    '''
    Get user's posts in subreddit.

    Keyword arguments:
    post_history = list returned from get_post_history(user).
    subreddit = instance of Praw's subreddit class.

    Returns a list of : [title (str), date created (str), parent subreddit (Subreddit class), body text (str), number of comments (int) ]
    '''
    posts_in_subreddit = []
    for post in post_history:
        if post['subreddit'] == subreddit:
            posts_in_subreddit.append(post)
    return posts_in_subreddit

def get_comment_history(user):
    '''
    Get user's comment history.

    Keyword arguments:
    user = an instance of Praw's redditor class.

    Returns a list: [date created, comment id (str), parent subreddit (Subreddit class), body text (str)]
    
    '''
    comment_history = []
    for comment in user.comments.new():
        temp = comment.subreddit
        x = {
            'id': comment.id,
            'created': comment.created_utc,
            'post': comment.submission.id,
            'subreddit': temp.display_name,
            'body': comment.body,
            'score': comment.score
        }
        comment_history.append(x)
    return comment_history

def get_comments_in_subreddit(comment_history, subreddit):
    '''
    Get user's comments in a subreddit.

    Keyword arguments:
    comment_history = list returned from get_comment_history(user).
    subreddit = instance of Praw's subreddit class.

    Returns a list: [date created, comment id (str), parent subreddit (Subreddit class), body text (str)]
    '''
    comments_in_subreddit = []
    for comment in comment_history:
        if comment["subreddit"] == subreddit.display_name:
            comments_in_subreddit.append(comment)
    return comments_in_subreddit

def get_upvote_history(user):
    upvote_history = []
    for comment in user.upvoted():
        temp = comment.subreddit
        x = {
            'id': comment.id,
            'created': comment.created_utc,
            'subreddit': temp.display_name,
            'body': comment.title
        }
        upvote_history.append(x)
        # print(comment.__class__)
        # pprint.pprint(vars(comment))
    return upvote_history
    
def get_downvote_history(user):
    downvote_history = []
    for comment in user.downvoted():
        temp = comment.subreddit
        x = {
            'id': comment.id,
            'created': comment.created_utc,
            'subreddit': temp.display_name,
            'body': comment.title
        }
        downvote_history.append(x)
        # print(comment.__class__)
        # pprint.pprint(vars(comment))
    return downvote_history

def getUpvotedSubreddits(upvotes):
    global sortedSubDict
    #get posts upvoted by user
    #user = reddit.redditor('kah277')
    # upvotedPosts = user.upvoted()

    #put subreddit name and upvote totals in dictionary
    subredditDict = {}

    for u in upvotes:
        sub = u['subreddit']
        if sub not in subredditDict:
            subredditDict[sub] = 1
        else:
            subredditDict[sub]+=1

    #sort it from highest count to lowest
    sortedSubDict = dict(sorted(subredditDict.items(), key=lambda x: x[1], reverse=True))
    return sortedSubDict
def getPostSubreddits(posts):
    global subredditPostDictionary 

    # posts = user.submissions.new(limit=None)

    #put subreddit name and upvote totals in dictionary
    subredditPostDict = {}

    for p in posts:
        sub = p['subreddit']
        if sub not in subredditPostDict:
            subredditPostDict[sub]=1
        else:
            subredditPostDict[sub]+=1

    #sort it from highest count to lowest
    subredditPostDictionary  = dict(sorted(subredditPostDict.items(), key=lambda x: x[1], reverse=True))
    return subredditPostDictionary 
def getCommentSubreddits(comments):
    global subredditCommentDictionary
    #get posts upvoted by user
    #user = reddit.redditor('kah277')
    # comments = user.comments.new(limit=None)

    #put subreddit name and upvote totals in dictionary
    subredditCommentDict = {}

    for c in comments:
        sub = c['subreddit']
        if sub not in subredditCommentDict:
            subredditCommentDict[sub]=1
        else:
            subredditCommentDict[sub]+=1

    #sort it from highest count to lowest
    subredditCommentDictionary = dict(sorted(subredditCommentDict.items(), key=lambda x: x[1], reverse=True))
    return subredditCommentDictionary
