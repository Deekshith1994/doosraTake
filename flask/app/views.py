from flask import render_template, url_for, flash, redirect, request
from app import app, bcrypt, db
from app.forms import RegistrationForm, LoginForm, IPLPostMatchReviewForm, SelectPostType
from app.models import User, Post
from flask_login import login_user, login_required, logout_user, current_user

# from firebase import firebase
# firebase = firebase.FirebaseApplication('https://doosratake-1da18.firebaseio.com/', None)
# new_user = 'Ozgur Vatansever'
# result = firebase.post('/users', new_user, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
# print (result)

# result = firebase.post('/users', new_user, {'print': 'silent'}, {'X_FANCY_HEADER': 'VERY FANCY'})
# print (result == None)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home/")
# @login_required
def home():
    posts = Post.query.all()
    userName = ''
    if current_user.is_authenticated :
        userName = current_user.username
    return render_template("/public/home.html", title='Home', posts=posts, isAuthenticated = current_user.is_authenticated, user = userName)
    

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("/public/login.html", title='Login', form=form)


@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created, please login!', 'success')
        return redirect(url_for('login'))
    return render_template("/public/register.html", title='Reg', form=form)



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
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('/public/create_ipl_postMatchReview.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/iplPostMatchReview/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('/public/post.html', title=post.title, post=post)


@app.route("/iplPostMatchReview/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = IPLPostMatchReviewForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('/public/create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
