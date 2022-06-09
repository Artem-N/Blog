from flask_login import current_user, login_user, logout_user, login_required
from flask import abort

from app import fapp, render_template, request, redirect, url_for, db

from app.models import User, Post
from app.forms import RegisterForm, LoginForm, PostForm


@fapp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        login_user(user=user)

        next_url = request.args.get('next', url_for('index'))
        return redirect(next_url)

    return render_template('login.html', title='Sing in', form=login_form)


@fapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@fapp.route('/register', methods=['GET', 'POST'])
def register():

    reg_form = RegisterForm()
    message = None

    if reg_form.validate_on_submit():

        user = User(username=reg_form.username.data, password=reg_form.password.data, email=reg_form.email.data)
        db.session.add(user)
        db.session.commit()
        message = 'User successfully registered!'

        next_url = request.args.get('next', url_for('login'))
        return redirect(next_url)

    return render_template('register.html', form=reg_form, title='Sing up', message=message)


@fapp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():

    form = PostForm()
    if form.validate_on_submit():
        created_post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(created_post)
        db.session.commit()
        next_url = request.args.get('next', url_for('index'))
        return redirect(next_url)

    return render_template('create_post.html', title='New Post', form=form)


@fapp.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    current_post = Post.query.get(post_id)
    if current_user.is_authenticated:
        next_url = request.args.get('next', url_for('index'))
        return redirect(next_url)

    return render_template('post.html', title='Post', post=current_post)


@fapp.route('/post/<post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post_to_update = Post.query.get(post_id)
    if post_to_update.author != current_user:
        abort(403)# only the owner of the post can edit it!
    form = PostForm()
    if form.validate_on_submit():
        post_to_update.title = form.title.data
        post_to_update.body = form.body.data
        db.session.commit()
        return redirect(url_for('post', post_id=post_to_update))
    elif request.method == 'GET':
        form.title.data = post_to_update.title
        form.title.data = post_to_update.body
    return render_template('edit_post.html', title='Updated Post', form=form)


@fapp.route('/post/<post_id>/delete', methods=['GET'])
def delete_post(post_id):

    post_to_delete = Post.query.get(post_id)

    db.session.delete(post_to_delete)
    db.session.commit()

    return redirect(url_for('index'))


@fapp.route('/')
@fapp.route('/index')
@login_required
def index():
    # if 'keyword' in request.args:
    #     keyword = request.args['keyword']
    #     posts = Post.query.filter(Post.title.like(f'{keyword}')).order_by(Post.timestamp.desc()).all()
    # else:
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)


@fapp.route('/blog/info/<category>/<page>/<post_id>')
def blog_info(category, page, post_id):
    return f'Blog content here - {category}: {page}: {post_id}'

