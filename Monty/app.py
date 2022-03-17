from flask import Flask, render_template, request, url_for
import praw, datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#Database Models
class Subreddit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    subscriber_count = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return 'Subreddit %r>' % self.id

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id= db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    subreddit = db.Column(db.String(200), nullable=False)
    body_text = db.Column(db.String(1000), nullable=False)
    num_comments =db.Column(db.Integer(), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id= db.Column(db.Integer(), nullable=False)
    date_created = db.Column(db.Float(), nullable=False)
    parent_post = db.Column(db.String(100), nullable=False)
    parent_sub = db.Column(db.String(100),nullable=False)
    body_text = db.Column(db.String(1000),nullable=False)

reddit = praw.Reddit(client_id='-C_5_SM1bjiRC2J8_WhiYw',
    client_secret='sYt31Wej7bxpQDKWLtdNAOuweRYeEw',
    username='Thatcatisphat',
    user_agent='Python:RRSDTest:0.0.1 (by u/<Thatcatisphat>')

#Dummy Data
user = reddit.redditor('bytheshore81')

#--- Site Functions Start ----
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
            'body': comment.body
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
#---- Site Functions End ----


#---- Site Starts ----
@app.before_first_request
def populate_database():
    post_history = get_post_history(user)
    for post in post_history:
        new_post = Post(site_id = post['id'], title = post['title'], subreddit = post['subreddit'], body_text = post['body'], num_comments = post['num_comments'])
        db.session.add(new_post)
        db.session.commit()

    comment_history = get_comment_history(user)
    for comment in comment_history:
        new_comment = Comment(site_id =comment['id'], date_created =comment['created'], parent_post = comment['post'], parent_sub = comment['subreddit'], body_text = comment['body'])
        db.session.add(new_comment)
        db.session.commit()

@app.route('/')
def home():
    #placeholder top 10 logic
    return render_template('index.html')

@app.route('/subreddit/<name>')
def subreddit(name):
    #replace with database query
    post_history = get_post_history(user)
    comment_history = get_comment_history(user)

    posts_in_sub = get_posts_in_subreddit(post_history, reddit.subreddit(name))
    post_count = len(posts_in_sub)
    comments_in_sub = get_comments_in_subreddit(comment_history, reddit.subreddit(name))
    comment_count = len(comments_in_sub)
    sub_stats = get_subreddit_stats(reddit.subreddit(name))
    title = sub_stats['title']
    description = sub_stats['description']
    subscriber_count = sub_stats['subscriber_count']

    return render_template("subreddit.html", title = title, description = description, subscriber_count = subscriber_count, post_count = post_count, comment_count = comment_count)
    




if __name__ == "__name__":
    app.run(debug=True)
