from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

posts_arr = []
id = 0

def get_date():
    date = datetime.now()
    return date.strftime("%H:%M")

@app.route("/")
def home():
    return render_template("index.html", posts=posts_arr)

@app.route("/new-post")
def new_post():
    return render_template("make-post.html")

@app.route("/make-post", methods=['GET', 'POST'])
def get_post():
    global id
    if request.method == "POST":
        post_title = request.form.get("title")
        post_subtitle = request.form.get("subtitle")
        post_body = request.form.get("body")
        post_author = request.form.get("author")
        id+=1
        new_post = {
            "id": id,
            "title": post_title,
            "subtitle": post_subtitle,
            "body": post_body,
            "author": post_author,
            "date": get_date()
        }
        posts_arr.append(new_post)
    return render_template("index.html", posts=posts_arr[::-1])

@app.route("/edit-post/<int:post_id>")
def edit_post(post_id):
    desired_post = None
    for post in posts_arr:
        if post["id"] == post_id:
            desired_post = post
            break

    # Optional: Handle case when post is not found
    if desired_post is None:
        return "Post not found", 404  # or redirect to another page

    return render_template("make-post.html", post=desired_post)

@app.route("/save-edited/post/<int:post_id>", methods=["POST"])
def save_edited_post(post_id):
    title = request.form.get("title")
    subtitle = request.form.get("subtitle")
    body = request.form.get("body")
    author = request.form.get("author")
    for post in posts_arr:
        if int(post["id"]) == int(post_id):
            post["title"] = title
            post["subtitle"] = subtitle
            post["body"] = body
            post["author"] = author
    return render_template("index.html", posts=posts_arr)

@app.route("/delete-post/<int:post_id>")
def delete_post(post_id):
    for post in posts_arr:
        if int(post["id"]) == int(post_id):
            posts_arr.remove(post)
    return render_template("index.html", posts=posts_arr)

if __name__ == "__main__":
    app.run(debug=True)