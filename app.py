__author__ = 'george'

from flask import Flask, request, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel
from wtforms.validators import ValidationError
from flask.ext.user import current_user, login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask.ext.mail import Mail, Message
from decorators import async
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SECRET_KEY"] = "Super secret key no one will find"
app.config["CSRF_ENABLED"] = True
app.config["USER_ENABLE_USERNAME"] = True
app.config["USER_ENABLE_EMAIL"] = False
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 
app.config["MAIL_PASSWORD"] =
app.config["DEFAULT_MAIL_SENDER"] = '"Arctic Game Jam Team" <post@artcicgamejam.com>'
db = SQLAlchemy(app)
babel = Babel(app)
mail = Mail(app)
@babel.localeselector
def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default="")


def password_validator(form, field):
    password = field.data
    if len(password) < 4:
        raise ValidationError(_("Password must be at least 4 characters"))

class Person(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    age = db.Column(db.Integer)
    info = db.Column(db.Text)
    sex = db.Column(db.String)

    def __init__(self, name, email, age, info, sex):
        self.name = name
        self.email = email
        self.age = age
        self.info = info
        self.sex = sex

    def __repr__(self):
        return "<Person %s>" % self.name

db.create_all()
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, password_validator=password_validator)
user_manager.init_app(app)

@app.route("/ajax/register", methods=["POST"])
def register_user():
    if request.method == "POST":


        name = request.form["nameInput"]

        email = request.form["emailInput"]

        age = request.form["ageInput"]

        info = request.form["textarea"]

        sex = request.form["sex"]
        p = Person.query.filter_by(email=email).all()
        if p:
            return "400"
        p = Person.query.filter_by(name=name).all()
        if p:
            return "400"
        p = Person(name, email, age, info, sex)
        db.session.add(p)


        send_registerd_email(email)


        #db.session.commit()
        return "200"

@app.route("/index.html")
@app.route("/")
def show_index():
    num_participants = Person.query.count()
    available_spots = 40 - num_participants
    return render_template("index.html", available_spots=available_spots)

@app.route("/program.html")
@app.route("/program")
def show_program():
    return  render_template("program.html")
@app.route("/rules.html")
def show_rules():
    return render_template("rules.html")


@app.route("/register.html", methods=["POST", "GET"])
def show_register():
    return render_template("register.html")

@app.route("/stats.html")
@app.route("/stats")
@login_required
def stats():
    participants = Person.query.all()
    emails = [p.email for p in participants]
    print(emails)
    return render_template("stats.html", participants=participants, emails=emails)


@app.route("/logout")
@app.route("/logout.html")
@app.route("/login")
@app.route("/login.html")
def login():
    return render_template(url_for("user.login"))

def send_registerd_email(address):
    msg = Message("Welcome to Arctic Game Jam 2014", sender=("Arctic Game Jam team", "post@arcticgamejam.com"))
    msg.add_recipient(address)

    msg.html = render_template("email/welcome.html")
    msg.body = render_template("email/welcome.txt")
    send_email_async(msg)

@async
def send_email_async(msg):
    mail.send(msg)



if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0")