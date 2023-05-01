from flask import Flask, render_template, request
import requests

app = Flask(__name__)

post_json = requests.get("https://api.npoint.io/ca01e4f19c5ba9f73f70").json()


# for post in post_json:
#    post_obj = Post(post_id=post['id'], title=post['title'], subtitle=post['subtitle'], body=post['body'])
#    list_post_obj.append(post_obj)


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
    name = request.form["username"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    print(f"{name} \n {email} \n {phone} \n {message}")
    return render_template("contact.html", data=name)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in post_json:
        if int(blog_post["id"]) == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
