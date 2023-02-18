import os
import time
import json
from flask import Blueprint, render_template, request, flash, jsonify, request, abort
from flask_login import login_required, current_user
from . import db
from .models import Inventory
from werkzeug.utils import secure_filename
from script import process_csv



views = Blueprint('views', __name__)


ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = f'{filename.split(".")[0]}_{int(time.time())}.csv'
            savepath = "F:/Documents/Python Projects/flaskProject/Website/static/imports"
            save_location = os.path.join(savepath, new_filename)
            file.save(save_location)
            process_csv(save_location)
    return render_template("home.html", user=current_user)


@views.route('/api/data')
def data():
    current_user_discordid = current_user.discordid
    query = Inventory.query.filter_by(discordid=f'{current_user_discordid}')

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(
            Inventory.name.like(f'%{search}%'),
            Inventory.edition.like(f'%{search}%'),
            Inventory.foil.like(f'%{search}%')
        )
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in ['count', 'name', 'edition', 'foil']:
                name = 'name'
            col = getattr(Inventory, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'total': total,
    }

@views.route('/api/data', methods=['POST'])
def update():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    inventory = Inventory.query.get(data['id'])
    for field in ['count', 'name', 'edition', 'cardnumber', 'foil','discordid']:
        if field in data:
            setattr(inventory, field, data[field])
    db.session.commit()
    return '', 204

