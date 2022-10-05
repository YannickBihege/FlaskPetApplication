"""Flask Application for Paws Rescue Center."""
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    """View function for Home Page."""
    return render_template("home.html")


@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
