from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from flask_mailman import EmailMessage

views = Blueprint('views', __name__)

@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    if request.method == 'POST':
        sender_email = request.form.get('sender_email')
        recipient_email = request.form.get('recipient_email')
        subject = request.form.get('subject')
        email_body = request.form.get('email_body')

        if not sender_email or not recipient_email or not subject or not email_body:
            flash('Please fill in all fields', 'error')
            return render_template("compose.html", user=current_user)

        msg = EmailMessage(
            subject,
            email_body,
            sender_email,
            [recipient_email]
        )

        try:
            msg.send()
            flash('Email sent successfully', 'success')
        except Exception as e:
            flash(f'Error sending email: {str(e)}', 'error')

    return render_template("compose.html", user=current_user)