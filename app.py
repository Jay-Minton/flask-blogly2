"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "canilive"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def back_to_users():
    return redirect("/users")

@app.route('/users')
def list_users():
    """Shows all users in db"""
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def add_user():
    """Show new user form"""
    #users = User.query.all()
    return render_template('new_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Create new user"""
    new_user = User(first_name = request.form["first_name"], 
                    last_name = request.form["last_name"],
                    image_url = request.form["image_url"] or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single User"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Edit details about a single User"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_details.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Update details for a single User"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user.id}")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a user from the DB"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

"""Post routes down here"""

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Shows form to create a new post for a user"""
    user = User.query.get_or_404(user_id)
    return render_template("new_post.html", user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Creates a new post for a user""" 
    post = Post(title = request.form["title"], content = request.form["content"], user_id = user_id)  
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")
    
@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Shows form for editing a post"""
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)  

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Edit a post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows post info"""
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)


@app.route('/posts/<int:post_id>/delete',methods=["POST"])
def delete_post(post_id):
    """Delete a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")
    