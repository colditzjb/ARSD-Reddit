from flask import Flask 
from flask import render_template
import praw

app = Flask(__name__)  

reddit = praw.Reddit(client_id = 'lxxZ8MnuOIRjYHVORUBoww', client_secret = 'YgyBe6fKMiYl0_KZPuKuelNLcEMi9g', username='kah277', password='ghu735d1$', user_agent='rrsdv1')
 
@app.route('/')  
def index():  
    global sorted
    #get posts upvoted by user
    user = reddit.redditor('kah277')
    upvotedPosts = user.upvoted()

    #put subreddit name and upvote totals in dictionary
    subredditDict = {}

    for u in upvotedPosts:

        if u.subreddit.display_name not in subredditDict:
            subredditDict[u.subreddit.display_name] = 1
        else:
            subredditDict[u.subreddit.display_name]+=1

    #sort it from highest count to lowest
    sorted = dict(sorted(subredditDict.items(), key=lambda x: x[1], reverse=True))
    li = list(sorted.keys())
    upvoteCounts = list(sorted.values())

    return render_template('chart.html',subreddits=li, upvotes=upvoteCounts) #render_template('list.html',subreddits=li)
  
if __name__ =="__main__":  
    app.run(debug = True)  
