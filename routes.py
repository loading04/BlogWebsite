from datetime import date
from flask import render_template, request, redirect, flash, url_for, logout_user
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash
from config import *
from forms import *
from main import send_email
from models import *


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>", methods=['POST', 'GET'])
def show_post(post_id):
    form = CreateCommentForm()
    requested_post = db.session.get(entity=BlogPost, ident=post_id)

    if request.method == "POST":
        if current_user:
            comment = Comment(
                text=request.form.get("comment"),
                author_id=current_user.id,
                post_id=post_id
            )
            db.session.add(comment)
            db.session.commit()

    return render_template("post.html", post=requested_post, form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = CreateUserForm()

    if request.method == 'POST':
        new_user = User()
        new_user.email = request.form.get('email')
        find_user = db.session.query(User).filter_by(email=new_user.email).first()
        if find_user is not None:
            flash('email exists already go to Log in Page instead ')
        else:
            new_user.name = request.form.get('name')
            pwd_to_hash = request.form.get('password')
            hashed_pwd = generate_password_hash(password=pwd_to_hash, salt_length=8, method="pbkdf2:sha256")
            new_user.password = hashed_pwd

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = CreateLoginForm()

    if request.method == 'POST':
        email = request.form.get('email')
        get_password = request.form.get('password')
        user = db.session.query(User).filter_by(email=email).first()
        if user is None:
            flash('email not found go to register instead ')
        else:
            if check_password_hash(user.password, get_password):
                login_user(user)
                return redirect(url_for('get_all_posts'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():

    form = CreatePostForm()
    if form.validate_on_submit():
        if current_user:
            new_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                body=form.body.data,
                img_url=form.img_url.data,
                date=date.today().strftime("%B %d, %Y"),
                author_id=current_user.id

            )
        with app.app_context():
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form)


@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.session.get(entity=BlogPost, ident=post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<post_id>", methods=["POST", "GET"])
@admin_only
def delete_post(post_id):
    db.session.delete(db.session.get(entity=BlogPost, ident=post_id))
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route('/form-entry', methods=["POST"])
def receive_data():
    if request.method == "POST":
        data = request.form
        print(data)
        send_email(data["username"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", data=data["username"])
