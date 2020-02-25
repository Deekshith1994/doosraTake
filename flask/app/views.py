from flask import render_template, url_for, flash, redirect, request
from app import app, bcrypt
from app.forms import LoginForm, IPLPostMatchReviewForm, SelectPostType
from app.models import FireBaseUtil, User
from flask_login import login_user, login_required, logout_user, current_user

@app.route("/", methods=['GET', 'POST'])
@app.route("/home/")
def home():
    return render_template("/public/home.html", title='Home', posts=FireBaseUtil.getAllPosts())

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.user_id.data in ['rkallem', 'hagarwal', 'sgundu', 'akonidena', 'pverma'] and FireBaseUtil.getUserPassword(form.user_id.data) == form.password.data:
            user = User.getUser(form.user_id.data)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("/public/login.html", title='Login', form=form)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/public/profile/")
@login_required
def profile():
    return render_template('/public/profile.html', title='Account')

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = SelectPostType()
    if form.validate_on_submit():
        return redirect(url_for('new_IPLPostMatchReview'))

    return render_template('/public/create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/IPL_MatchReview", methods=['GET', 'POST'])
@login_required
def new_IPLPostMatchReview():
    form = IPLPostMatchReviewForm()
    if form.validate_on_submit():
        FireBaseUtil.createPost(title=form.title.data, content=form.content.data, name=current_user.name, username=current_user.id)
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('/public/create_ipl_postMatchReview.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/iplPostMatchReview/<string:post_id>")
def post(post_id):
    post = FireBaseUtil.getPost(post_id)
    userName = ''
    if current_user.is_authenticated : 
        userName = current_user.username
    return render_template('/public/post.html', title=FireBaseUtil.getPost(post_id).get('title'), current_user = userName, post=post)


@app.route("/iplPostMatchReview/update/<string:post_id>", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = FireBaseUtil.getPost(post_id)
    form = IPLPostMatchReviewForm()
    if form.validate_on_submit():
        FireBaseUtil.updatePost(title=form.title.data, content=form.content.data, post=post)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.get('id')))
    elif request.method == 'GET':
        form.title.data = post.get('title')
        form.content.data = post.get('content')
    return render_template('/public/update_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<string:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    FireBaseUtil.removePost(post_id)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
