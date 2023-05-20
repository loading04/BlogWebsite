from datetime import date
import smtplib
import os
from functools import wraps
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditor, CKEditorField
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

OWN_EMAIL = os.getenv("OWN_EMAIL")
OWN_PASSWORD = os.getenv("OWN_PASSWORD")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(entity=User, ident=user_id)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


# with app.app_context():
#    db.create_all()


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class CreateUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Register")


class CreateLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# HTTP GET - Read Record


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = db.session.get(entity=BlogPost, ident=post_id)
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


## todo login page
## todo stay connected

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
            password = user.password
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
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=form.author.data,
            date=date.today().strftime("%B %d, %Y")
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
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
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


def send_email(username, email, phone, message):
    MY_EMAIL = OWN_EMAIL
    TO_EMAIL = OWN_EMAIL
    My_PASSWORD = OWN_PASSWORD

    msg = f"\nName: {username}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(MY_EMAIL, My_PASSWORD)
    mail.sendmail(MY_EMAIL, TO_EMAIL, msg)
    mail.quit()


if __name__ == "__main__":
    app.run(debug=True)
