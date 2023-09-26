"""Blogly application."""
# Set up virtual environment

from flask import Flask, render_template, request, redirect, url_for
from models import db, connect_db, User #, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thesecret_keygoeshere'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)
db.create_all()

# =======================================================================
@app.route("/")
def homepage():
    tablename=User.__tablename__
    users=User.query.order_by(User.first_name, User.last_name).all()
    return render_template("homepage.html",
                           tablename=tablename,
                           users=users)

@app.route("/users/new", methods=["GET"])
def add_user():
    return render_template("createuser.html")

@app.route("/users/new", methods=["POST"])
def create_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/")

# Need to create a route that will go to the specific users profile.
@app.route("/users/<int:user_id>")
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("userprofile.html", 
                           user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edituser.html", 
                           user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect("/")

@app.route("/users/<int:user_id>/delete", methods=["GET", "POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

# # =============================================================================
if __name__ == "__main__":
    app.run(debug=True)