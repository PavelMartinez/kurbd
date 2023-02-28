import os.path

from flask import Blueprint, request, render_template, current_app
from database.operations import select
from database.sql_provider import SQLProvider
from access import group_required


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
print(" Provider path : " + os.path.join(os.path.dirname(__file__), 'sql'))
print(" os.path.dirname(__file__) : " + os.path.dirname(__file__))


@blueprint_query.route('/test')
def provider_test():
    p = os.path
    print(p)
    p1 = os.path.dirname(__file__)
    print(p1)
    return 'None'



@blueprint_query.route('/menu_queries')
@group_required
def menu_queries():
    return render_template('menu_queries.html')

@blueprint_query.route('/query1')
@group_required
def query1():
    print(os.path.join(os.path.dirname(__file__)))
    _sql = provider.get('query1.sql')
    product_result, schema = select(current_app.config['db_config'], _sql)
    if len(product_result) == 0:
        return render_template('not_found.html')
    return render_template('db_result.html', schema=['Фильм', 'Выручка'], result=product_result, query_numb="Query1")

@blueprint_query.route('/query2', methods=['GET', 'POST'])
@group_required
def query2():
    print(os.path.join(os.path.dirname(__file__)))
    if request.method == 'POST':
        input_year = request.form.get('product_name')
        if input_year:
            _sql = provider.get('query2.sql', input_year=input_year)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) == 0:
                return render_template('not_found.html')
            return render_template('db_result.html', schema=['Фильм', 'Кол-во просмотров'], result=product_result, query_numb="Query2")
        else:
            return render_template('not_found.html')
    elif request.method == 'GET':
        return render_template('query.html', ph_title="Введите год", title_name='Query2')








































"""
                Тут чисто блупринт запросов
                Тут все просто 
                Первая функция для 1 запроса
                Вторая функция для 2
"""