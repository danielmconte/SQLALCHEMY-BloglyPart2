from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_redirect():
    return redirect('/users')

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def new_form():
    return render_template('new_user_form.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def detail_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(id_code = user.id).all()
    return render_template("details.html", user=user, posts = posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url= image_url

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')

# Part 2 Adding Posts

@app.route('/users/<int:user_id>/posts/new')
def post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_post(user_id):
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, id_code=user_id)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_first = post.user.first_name
    user_last = post.user.last_name
    return render_template("post.html", post = post, user_first = user_first, user_last=user_last)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post_form.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def post_edit_form(post_id):
    title = request.form["title"]
    content = request.form["content"]

    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    post_code = post.id_code
    postly = Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users/{post_code}")

# Part 3 Adding Tags

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tags(tag_id):
    directory = db.session.query(PostTag.tag_id, PostTag.post_id, Post.title).outerjoin(Post).all()
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag= tag, posts=directory)

@app.route('/tags/new')
def new_tag_form():
    return render_template('new_tag_form.html')

@app.route('/tags/new', methods=["POST"])
def post_new_tag():
    tag_name = request.form["tag_name"]

    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_tag_edit_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_edit_form.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def post_tag_edit_form(tag_id):
    tag_name = request.form["tag_name"]


    tag = Tag.query.get_or_404(tag_id)

    tag.name = tag_name

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags")

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect("/tags")

    #need to add tags on post.html, tag checkboxes on Add Post, and Edit Post 



