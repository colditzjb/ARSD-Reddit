import praw

reddit = praw.Reddit(client_id = 'lxxZ8MnuOIRjYHVORUBoww', client_secret = 'YgyBe6fKMiYl0_KZPuKuelNLcEMi9g', username='kah277', password='ghu735d1$', user_agent='rrsdv1')

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

#print the top 10
li = list(sorted.keys())
if len(li) <= 10:
    for x in li:
        print(x)
else:
    for x in range(10):
        print(li[x])
