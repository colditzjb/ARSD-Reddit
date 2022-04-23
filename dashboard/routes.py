#Need flask/flask_login packages below, flask-sqlalchemy, and psychopg2 installed in working python environment

from dashboard import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import praw, random
from dashboard.models import User
# Import dashboard python functions
from dashboard import stats
import numpy as np
from dashboard import db
import time

scope_input = 'history, identity, read'
scopes = [scope.strip() for scope in scope_input.strip().split(",")]

reddit = praw.Reddit(
    client_id = 'tC-RStYYMyOXAVgtuVy3cA',
    client_secret = 'XIJwrc-zKpm-kMB7aR0MCE3DvDGpRw',
    redirect_uri="http://127.0.0.1:5000/auth",
    user_agent="obtain_refresh_token testing by u/Solid-Guidance1826 Im sorry, Im bad at this. contact:henryp959@gmail.com",
)
state = str(random.randint(0, 65000))

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return redirect(reddit.auth.url(scopes, state, "temporary"))

@app.route('/auth')
def auth():
    code = request.args.get('code')
    print('code:', code)
    print(reddit.auth.authorize(code))
    print(reddit.user.me())
    uname = str(reddit.user.me())
    user = User.query.filter_by(username=uname).first()
    if user:
        login_user(user)
        flash(f"Welcome back. You are logged in as {user.username}", category='success')
        print(f"Welcome back. You are logged in as {user.username}")
    else:
        user = User(username=uname)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Account successfully created. You are logged in as {user.username}", category='success')
        print(f"Account successfully created. You are logged in as {user.username}")
    return redirect(url_for('home_page'))

@app.route('/support_subs')
def show_support_subs():
    subsDict = stats.getSupportSubs()
    return render_template('support_subs.html', subsDict = subsDict)

@app.route('/dashboard')
@login_required
def dashboard_page():
    # if type(comments) == 'NoneType':
    #     return render_template(url_for('error_page'))

    start = time.time()
    #Pull data from these objects
    submissions = stats.get_post_history(reddit.user.me())
    comments = stats.get_comment_history(reddit.user.me())
    #this only gets submissions
    upvotedSubmissions = stats.get_upvote_history(reddit.user.me())
    downvotedSubmissions = stats.get_downvote_history(reddit.user.me())
    # upvotesBySubreddit = stats.getUpvotedSubreddits(reddit.user.me())
    upvotesBySubreddit = stats.getUpvotedSubreddits(upvotedSubmissions)
    end = time.time()
    print(f'after object creation functions {end - start}')
    # Henry's code

    #Data for the graph that shows comments on given days of the week (useless)
    jsdict = stats.postingActivityDay(comments)
    #this returns two dictionaries with frequencies organized by subreddit(comments and submissions)
    topSubs = stats.activityCountSubreddit(comments, submissions)
    #Returns the average number of characters per comment
    avgStats = stats.averageCommentLengthSupport(comments)
    #Gets the subreddit the user commented on the most
    maxComment, maxComNum = stats.getMax(topSubs[0])
    #Gets the subreddit the user posted the most
    maxSubmission, maxSubNum = stats.getMax(topSubs[1])
    #Gets the subreddit the user upvoted the most(submissions only)
    maxUpvote, maxUpNum = stats.getMax(upvotesBySubreddit)
    maxStats = [[maxComment,maxComNum] ,[maxSubmission,maxSubNum], [maxUpvote,maxUpNum]]
    AccountAge = stats.getAccountAge(reddit.user.me())
    #returns average number of comments made on days commented at least once
    #add average comments per day using age of acc / # comments and add the data below after
    daysEngaged = stats.commentsOnDaysEngaged(comments)
    #gets data for wordcloud
    cloudData = stats.wordsDict(comments, 35)
    mainRecoverySub = stats.getMax(topSubs[0])
    mainRecoverySub = mainRecoverySub[0]
    bestComment = stats.getBestComment(comments)
    worstComment = stats.getWorstComment(comments)
    weeklyComments = stats.weeklyComments(comments)
    # if(len(bestComment['body']) > 200):
    #     comBody = bestComment['body'][0:200] + '...'

    sortedSubDict = stats.getUpvotedSubreddits(upvotedSubmissions)
    li = list(sortedSubDict.keys())
    upvoteCounts = list(sortedSubDict.values())     

    subredditPostDictionary = stats.getPostSubreddits(submissions)
    postKeys = list(subredditPostDictionary.keys())
    postValues = list(subredditPostDictionary.values()) 

    subredditCommentDictionary = stats.getCommentSubreddits(comments)
    commentKeys = list(subredditCommentDictionary.keys())
    commentValues = list(subredditCommentDictionary.values()) 
	
    daysact, postact = stats.activityStats(submissions, comments, upvotedSubmissions, downvotedSubmissions)


    allRRSubreddits_List = ["stopdrinking", "RedditorsinRecovery", "alcoholism", "addiction", "AtheistTwelveSteppers", "secularsobriety", "addictionprevention", "alcoholicsanonymous", "ResearchRecovery", "Alcoholism_Medication", "cutdowndrinking", "dryalcoholics", "recoverywithoutAA", "cripplingalcoholism"]

    return render_template('dashboard.html',jsdict=jsdict,topSubs=topSubs,avgStats=avgStats,
            li=li,upvoteCounts=upvoteCounts,maxStats=maxStats, cloudData=cloudData, daysEngaged=daysEngaged, 
            bestComment=bestComment, worstComment=worstComment,weeklyComments=weeklyComments,
            mainRecoverySub=mainRecoverySub,
             postKeys=postKeys, postValues=postValues, commentKeys=commentKeys, commentValues=commentValues,
            totalDays = AccountAge, days = daysact, post = postact, allRRSubreddits_List = allRRSubreddits_List)

@app.route('/subreddit/<name>')
def subreddit(name):
    #replace with database query
    post_history = stats.get_post_history(reddit.user.me())
    comment_history = stats.get_comment_history(reddit.user.me())
    posts_in_sub = stats.get_posts_in_subreddit(post_history, reddit.subreddit(name))
    post_count = len(posts_in_sub)
    comments_in_sub = stats.get_comments_in_subreddit(comment_history, reddit.subreddit(name))
    comment_count = len(comments_in_sub)
    sub_stats = stats.get_subreddit_stats(reddit.subreddit(name))
    title = sub_stats['title']
    description = sub_stats['description']
    subscriber_count = sub_stats['subscriber_count']  
    
    return render_template("subreddit.html", title = title, description = description, subscriber_count = subscriber_count, post_count = post_count, comment_count = comment_count)

    
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))





