from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from flask_mailman import EmailMessage

views = Blueprint('views', __name__)

@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('compose')
@login_required
def compose_msg():
    msg = EmailMessage(
            "Here's the title!",
            "Body of the email",
            "joseph2blessing2015@fastmail.com",
            ["ilorimuideen0000@gmail.com"]
    )
    msg.send()

    return "sent messsage."