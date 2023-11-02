from flask import (
    Blueprint, render_template, request, flash
)

from app.db import get_db

bp = Blueprint('mail', __name__, url_prefix="/")

@bp.route('/', methods=['GET'])
def index():
    db, cursor = get_db()

    cursor.execute("SELECT * FROM email")
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
            pass
        else:
            for error in errors:
                flash(error)

    return render_template('mails/create.html')