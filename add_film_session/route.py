import os.path

from flask import Blueprint, request, render_template, current_app
from database.operations import select_dict, insert
from database.sql_provider import SQLProvider
from access import group_required


blueprint_add = Blueprint('bp_add', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_add.route('/', methods=['GET'])
@group_required
def start_page():
    _sql = provider.get('start_page.sql')
    products = select_dict(current_app.config['db_config'], _sql)
    return render_template('start_page.html', products=products)

@blueprint_add.route('/', methods=['POST'])
@group_required
def edit_film_sessions():
    action = request.form.get('action')
    prod_id = request.form.get('prod_id')
    date_id = request.form.get('date_id')
    print(date_id)
    coef = request.form.get('Coefficient')
    place_id = request.form.get('id_place')
    if action == 'add_prod':
        message = add_session(prod_id, date_id, coef, place_id)
        print(message)
        return render_template('update_ok1.html', message=message)
    else:
        print("ErrNo4")
        return "Что-то пошло не так!"

def add_session(prod_id, date_id, coef, place_id):
    _sql = provider.get('add_session.sql', prod_id=prod_id, date_id=date_id, coef=coef, place_id=place_id)
    result = insert(current_app.config['db_config'], _sql)
    print("result3 = ", result)
    message = 'Упс! Что-то не так!'
    if result:
        message = 'Сеанс добавлен в базу данных'
    return message