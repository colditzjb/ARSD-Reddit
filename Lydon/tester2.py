from flask import Flask
from flask import render_template
from datetime import time
 
app = Flask(__name__)
import praw
#reddit = praw.Reddit(client_id = 'lxxZ8MnuOIRjYHVORUBoww', client_secret = 'YgyBe6fKMiYl0_KZPuKuelNLcEMi9g', username='kah277', password='ghu735d1$', user_agent='rrsdv1')
reddit = praw.Reddit(client_id = '9vMgH92jiZRkqWOv53H01w', client_secret = '7nevQp2kiEM06FfVElNq2UrHz3JH2Q', username='WaitDowntown8778', password='abcd4321', user_agent='test')
user = reddit.redditor('WaitDowntown8778')
#posts = user.upvoted()
posts = user.submissions.new(limit=None)
comments = user.comments.new(limit=None)
overall = posts and comments;
# comments = user.commented()
subredditDictionary={}
subredditPostDictionary = {}
subredditCommentDictionary={}
for p in posts:
    if p.subreddit.display_name not in subredditPostDictionary:
            subredditPostDictionary[p.subreddit.display_name]=1
    else:
            subredditPostDictionary[p.subreddit.display_name]+=1

for c in comments:
    if c.subreddit.display_name not in subredditCommentDictionary:
            subredditCommentDictionary[c.subreddit.display_name]=1
    else:
            subredditCommentDictionary[c.subreddit.display_name]+=1
            
for o in overall:
    if o.subreddit.display_name not in subredditDictionary:
            subredditDictionary[o.subreddit.display_name]=1
    else:
            subredditDictionary[o.subreddit.display_name]+=1

sortedList = dict(sorted(subredditDictionary.items(), key=lambda x: x[1], reverse=True))
sortedPostList = dict(sorted(subredditPostDictionary.items(), key=lambda x: x[1], reverse=True))
sortedCommentList = dict(sorted(subredditCommentDictionary.items(), key=lambda x: x[1], reverse=True))
topOverall=list(sortedList.keys())
topPosts=list(sortedPostList.keys())
topComments=list(sortedCommentList.keys())
#if len(topPosts) <= 10:
#    for x in topPosts:
#        print(x)
#else:
#    for x in range(10):
#        print(topPosts[x])
#print()
#if len(topComments) <= 10:
#    for x in topComments:
#        print(x)
#else:
#    for x in range(10):
#        print(topComments[x])
#print()
#if len(topOverall) <= 10:
#for x in topOverall:
#        print(x)
#else:
#    for x in range(10):
#        print(topOverall[x])
#print()
overall_keys = list(subredditDictionary.keys())
overall_values = list(subredditDictionary.values())
post_keys = list(subredditPostDictionary.keys())
post_values = list(subredditPostDictionary.values())
comment_keys = list(subredditCommentDictionary.keys())
comment_values = list(subredditCommentDictionary.values())

@app.route("/simple_chart")
def chart1():
    legend = 'Total'
    labels = overall_keys
    values = overall_values
    return render_template('chart.html', title='Total',max='10',labels=labels,values=values)

@app.route("/simple_chart2")
def chart2():
    legend = 'Number of Posts'
    labels = post_keys

    values = post_values
    return render_template('chart2.html', title='Number of Posts',max='10',labels=labels,values=values)
@app.route("/simple_chart3")
def chart3():
    legend = 'Number of Comments'
    labels = comment_keys

    values = comment_values
    return render_template('chart3.html', title='Number of Comments',max='10',labels=labels,values=values)
 
if __name__ == '__main__':
    app.run(debug=True)
