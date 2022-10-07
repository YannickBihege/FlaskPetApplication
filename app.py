"""Flask Application for Paws Rescue Center."""
from forms import SignUpForm, LoginForm
from flask import Flask, render_template, abort, request
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# csrf Token :) Please do not do share this in production
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
db = SQLAlchemy(app)


"""Information regarding the Pets in the System."""
Pets = [
    {"id": 1, "name": "Nelly", "age": "5 weeks",
        "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."},
    {"id": 2, "name": "Yuki", "age": "8 months",
     "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
    {"id": 3, "name": "Basker", "age": "1 year",
     "bio": "I love barking. But, I love my friends more."},
    {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."},
]

"""Information regarding the Users in the System."""
Users = [
    {"id": 1, "full_name": "Pet Rescue Team",
        "email": "team@pawsrescue.co", "password": "adminpass"},
]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    #
    rescuedPets = db.relationship('Pet')


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    age = db.Column(db.Integer,   nullable=False)
    bio = db.Column(db.String, nullable=False)
    rescuerId = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)


with app.app_context():
    db.create_all()


@app.route("/")
def homepage():
    """View function for Home Page."""
    return render_template("home.html", pets=Pets)


@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html",  pets=Pets)


@app.route("/details/<int:pet_id>")
def pet_details(pet_id):
    """View function for Showing Details of Each Pet."""
    pet = next((pet for pet in Pets if pet["id"] == pet_id), None)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    return render_template("details.html", pet=pet)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """View function for Showing Details of Each Pet."""
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = {"id": len(Users)+1, "full_name": form.full_name.data,
                    "email": form.email.data, "password": form.password.data}
        Users.append(new_user)
        return render_template("signup.html", message="Successfully signed up")
    return render_template("signup.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = next((user for user in Users if user["email"] ==
                    form.email.data and user["password"] == form.password.data), None)
        if user is None:
            return render_template("login.html", form=form, message="Wrong credentials. Please try again.")

        else:
            # add user to session
            session['user'] = user
            # render telplate
            return render_template("login.html", form=form, message="Successfully logged in")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')

    return redirect(url_for('homepage', _scheme='https', _external=True))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
