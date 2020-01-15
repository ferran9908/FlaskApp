from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default="Unknown Author")
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)

allPosts = [{
    "name":"Post 1",
    "content":"This is post 1",
    "author":"Ferran"
},
{
    "name":"Post 2",
    "content":"This is post 2",
}
]

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/posts', methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        postTitle = request.form['title']
        postAuthor = request.form['author']
        postContent = request.form['content']
        newPost = BlogPost(title=postTitle,content=postContent,author=postAuthor)
        db.session.add(newPost)
        db.session.commit()
        return redirect('/posts')
    else:
        allPosts = BlogPost.query.order_by(BlogPost.datePosted).all()
        return render_template('posts.html',posts = allPosts)


if __name__ == "__main__":
    app.run(debug=True)