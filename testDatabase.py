from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# set the config variable SQLALCHEMY_DATABASE_URI to point to this file.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# intialize the database connection
db = SQLAlchemy(app)


# Step create a model
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


with app.app_context():
    '''
    The create_all() command should be called after the models are declared. If the models 
    are defined in a separate module, then they should be imported first. Furthermore, 
    during development, if new models are created, then this command only creates the newly defined models.
    '''
    #  model that we just made will be created in the database
    db.create_all()
    '''
    a'' Initialize the database'''
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
        print('commit successful')
    except Exception as e:
        db.session.rollback()
    finally:
        db.session.close()
    # filter_by() is called and the password is given as a keyword argument. followd by .first() or all()
    # filter takes an expression as parameter
    # query .get takes the primary key as argument only
    print(Pet.query.all())
