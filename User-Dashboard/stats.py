
from datetime import datetime
import numpy as np

def postingActivityDay(reddit):
    supportSubs = ['test', 'videos','pcgaming']
    DoTW = {'Sunday': 1, 'Monday': 3, 'Tuesday': 2, 'Wednesday': 1, 'Thursday': 3, 'Friday': 2, 'Saturday': 2,}
    comments =  reddit.user.me().comments.new(limit=50)
    for comment in comments:
        if(str(comment.subreddit) in supportSubs):
            unix_val = datetime.fromtimestamp(comment.created)
            day = unix_val.weekday()
            if(day == 0): day = 'Sunday'
            elif(day == 1): day = 'Monday'
            elif(day == 2): day = 'Tuesday'
            elif(day == 3): day = 'Wednesday'
            elif(day == 4): day = 'Thursday'
            elif(day == 5): day = 'Friday'
            elif(day == 6): day = 'Saturday'
            if(day in DoTW):
                DoTW[day] += 1
    return DoTW


def topTenSubreddits(reddit):
    subList = {}
    comments =  reddit.user.me().comments.new(limit=500)
    for comment in comments:
        if(str(comment.subreddit) in subList):
            subList[str(comment.subreddit)] += 1
        else:
            subList[str(comment.subreddit)] = 1
    topSubs = sorted(subList, key=subList.get, reverse=True)[:10]
    return subList
#I should probably change this to also compile a list of submissions
#also this all will probably need to be changed to pull this from a database
def averageCommentLengths(reddit):
    commentLengths = []
    supportSubs = ['test', 'videos','pcgaming']
    wordsMain = {}
    comments =  reddit.user.me().comments.new(limit=50)
    for comment in comments:
        if(str(comment.subreddit) in supportSubs):
            body = str(comment.body)
            wordList = body.split()
            for word in wordList:
                if word not in wordsMain:
                    wordsMain[word] = 1
                else:
                    wordsMain[word] += 1
            # if(len(body) > 5): to remove short replies from average
            commentLengths.append(len(body))

    # print(len(commentLengths))
    avg = np.average(commentLengths)
    median = np.median(commentLengths)
    # print("Average: " , avg)
    # print("Median: " , median)
    output = []
    output.append(avg) 
    output.append(median)
    output.append(commentLengths)
    output.append(wordsMain)
    return output