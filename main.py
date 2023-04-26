from flask import Flask, render_template
from post import Post
import requests

app = Flask(__name__)

list_post_obj = []

post_json = requests.get("https://api.npoint.io/ca01e4f19c5ba9f73f70").json()

for post in post_json:
    post_obj = Post(post_id=post['id'], title=post['title'], subtitle=post['subtitle'], body=post['body'])
    list_post_obj.append(post_obj)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")



@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in list_post_obj:
        if int(blog_post.id) == index :
            requested_post = blog_post
            return render_template("post.html", post=requested_post)

    return "<h1>404 not found</h1>"



if __name__ == "__main__":
    app.run(debug=True)
