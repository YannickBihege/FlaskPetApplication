"""Flask Application for Paws Rescue Center."""
from forms import EditPetForm, SignUpForm, LoginForm
from flask import Flask, render_template, abort, request
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# csrf Token :) Please do not do share this in production
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
db = SQLAlchemy(app)


with app.app_context():

    """Model for Pets."""
    class Pet(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, unique=True)
        age = db.Column(db.String)
        bio = db.Column(db.String)
        posted_by = db.Column(db.String, db.ForeignKey('user.id'))

    """Model for Users."""
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        full_name = db.Column(db.String)
        email = db.Column(db.String, unique=True)
        password = db.Column(db.String)
        pets = db.relationship('Pet', backref='user')

    db.create_all()
    ''' Initialize the database'''
    # Create "team" user and add it to session
    team = User(full_name="Pet Rescue Team",
                email="team@petrescue.co", password="adminpass")
    db.session.add(team)

    # Create all pets
    nelly = Pet(name="Nelly", age="5 weeks",
                bio="I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.")
    yuki = Pet(name="Yuki", age="8 months",
               bio="I am a handsome gentle-cat. I like to dress up in bow ties.")
    basker = Pet(name="Basker", age="1 year",
                 bio="I love barking. But, I love my friends more.")
    mrfurrkins = Pet(name="Mr. Furrkins", age="5 years",
                     bio="Probably napping.")

    # Add all pets to the session
    db.session.add(nelly)
    db.session.add(yuki)
    db.session.add(basker)
    db.session.add(mrfurrkins)

    # Commit changes in the session
    try:
        db.session.commit()
        print('Pets and Users objects commited')
    except Exception as e:
        db.session.rollback()
    finally:
        db.session.close()


@app.route("/")
def homepage():
    """View function for Home Page."""
    pets = Pet.query.all() # get from database
    return render_template("home.html", pets=pets)


@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")


@app.route("/details/<int:pet_id>")
def pet_details(pet_id):
    """View function for Showing Details of Each Pet."""
    #pet = next((pet for pet in Pets if pet["id"] == pet_id), None)
    form = EditPetForm()
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    if form.validate_on_submit():
        pet.name= form.name.data
        pet.age = form.age.data
        pet.bio = form.bio.data
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("details.html" , pet = pet, form = form)

    return render_template("details.html", pet=pet, form = form)


@app.route("/delete/<int:pet_id>")
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None: 
        abort(404, description="No Pet was Found with the given ID")
    db.session.delete(pet)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('homepage', _scheme='https', _external=True))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """View function for Showing Details of Each Pet."""
    form = SignUpForm()
    if form.validate_on_submit():
        # new_user = {"id": len(users)+1, "full_name": form.full_name.data, "email": form.email.data, "password": form.password.data}
        # users.append(new_user)
        new_user = User(full_name=form.full_name.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form=form, message="This Email already exists in the system! Please Log in instead.")
        finally:
            db.session.close()
        return render_template("signup.html", message="Successfully signed up")
    return render_template("signup.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data), None)
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user is None:
            return render_template("login.html", form = form, message = "Wrong Credentials. Please Try Again.")
        else:
            # session['user'] = user
            session['user'] = user.id
            return render_template("login.html", message = "Successfully Logged In!")
    return render_template("login.html", form = form)


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')

    return redirect(url_for('homepage', _scheme='https', _external=True))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
