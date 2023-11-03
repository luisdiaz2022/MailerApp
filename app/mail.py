from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, current_app
)
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText

from app.db import get_db

bp = Blueprint('mail', __name__, url_prefix="/")

@bp.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    db, cursor = get_db()
    if search is None:
        cursor.execute("SELECT * FROM email")

    else:
        cursor.execute("SELECT * from email WHERE content like %s", ('%' + search + '%',))
    
    mails = cursor.fetchall()

    return render_template('mails/index.html', mails=mails)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []

        if not email:
            errors.append('Correo es obligatorio')
        if not subject:
            errors.append('Asunto es obligatorio')
        if not content:
            errors.append('Contenido es obligatorio')

        if len(errors) == 0:
            send(email, subject, content)
            db, cursor = get_db()
            cursor.execute("INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)", (email, subject, content))
            db.commit()

            return redirect(url_for('mail.index'))
        else:
            for error in errors:
                flash(error)

    return render_template('mails/create.html')


def send(to, subject, content):
    email_from = current_app.config['FROM_EMAIL']
    email_password = current_app.config['GOOGLE_API_KEY']
    email_to = to
    email_subject = subject
    email_content = MIMEText(content, 'plain')

    email_sender = EmailMessage()
    email_sender['From'] = email_from
    email_sender['To'] = email_to
    email_sender['subject'] = email_subject
    email_sender.set_content(email_content)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_from, email_password)
        smtp.sendmail(email_from, email_to, email_sender.as_string())