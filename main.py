from flask import Flask, render_template, request
import requests
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

post_json = requests.get("https://api.npoint.io/ca01e4f19c5ba9f73f70").json()

OWN_EMAIL = os.getenv("OWN_EMAIL")
OWN_PASSWORD = os.getenv("OWN_PASSWORD")


@app.route('/')
def home():
    return render_template("index.html", list=post_json)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/form-entry', methods=["POST"])
def receive_data():
    if request.method == "POST":
        data = request.form
        print(data)
        send_email(data["username"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", data=data["username"])


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in post_json:
        if int(blog_post["id"]) == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


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
