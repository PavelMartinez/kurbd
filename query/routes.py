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

@blueprint_query.route('/query1', methods=['GET', 'POST'])
@group_required
def query1():
    print(os.path.join(os.path.dirname(__file__)))
    if request.method == 'POST':
        try:
            input_year = int(request.form.get('year'))
            input_month = int(request.form.get('month'))
        except ValueError:
            return render_template('not_found.html', error="Параметры запроса введены неверно! "
                                                           "Введите год в формате XXXX, месяц в формате XX")
        if input_year and input_month and 2000 < input_year <= 2023 and 0 < input_month <= 12:
            _sql = provider.get('query1.sql', input_year=input_year, input_month=input_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) == 0:
                return render_template('not_found.html', error='Ошибка, ничего не найдено!')
            return render_template('db_result.html', schema=['Фильм', 'Выручка'], result=product_result, query_numb="Query1")
        else:
            return render_template('not_found.html', error="Параметры запроса не введены, или введены неверно! "
                                                           "Введите год в формате XXXX, месяц в формате XX")
    elif request.method == 'GET':
        return render_template('query.html', ph_title1="Введите год", ph_title2="Введите месяц", title_name='Query1')

@blueprint_query.route('/query2', methods=['GET', 'POST'])
@group_required
def query2():
    print(os.path.join(os.path.dirname(__file__)))
    if request.method == 'POST':
        try:
            input_year = int(request.form.get('product_name'))
        except ValueError:
            return render_template('not_found.html', error="Параметры запроса введены неверно! "
                                                           "Введите год в формате XXXX")
        if input_year and 2000 < input_year <= 2023:
            _sql = provider.get('query2.sql', input_year=input_year)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) == 0:
                return render_template('not_found.html', error='Ошибка, ничего не найдено!')
            return render_template('db_result.html', schema=['Фильм', 'Кол-во просмотров'], result=product_result, query_numb="Query2")
        else:
            return render_template('not_found.html', error="Параметры запроса не введены, или введены неверно! "
                                                           "Введите год в формате XXXX")
    elif request.method == 'GET':
        return render_template('query.html', ph_title1="Введите год", title_name='Query2')


@blueprint_query.route('/query3', methods=['GET', 'POST'])
@group_required
def query3():
    print(os.path.join(os.path.dirname(__file__)))
    if request.method == 'POST':
        try:
            input_year = int(request.form.get('product_name'))
        except ValueError:
            return render_template('not_found.html', error="Параметры запроса введены неверно! "
                                                           "Введите год в формате XXXX")
        if input_year and 2000 < input_year <= 2023:
            _sql = provider.get('query3.sql', input_year=input_year)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) == 0:
                return render_template('not_found.html', error='Ошибка, ничего не найдено!')
            return render_template('db_result.html', schema=schema, result=product_result, query_numb="Query3")
        else:
            return render_template('not_found.html', error="Параметры запроса не введены, или введены неверно! "
                                                           "Введите год в формате XXXX")
    elif request.method == 'GET':
        return render_template('query.html', ph_title1="Введите год", title_name='Query3')


@blueprint_query.route('/query4', methods=['GET', 'POST'])
@group_required
def query4():
    print(os.path.join(os.path.dirname(__file__)))
    if request.method == 'POST':
        try:
            input_year = int(request.form.get('year'))
            input_month = int(request.form.get('month'))
        except ValueError:
            return render_template('not_found.html', error="Параметры запроса введены неверно! "
                                                           "Введите год в формате XXXX, месяц в формате XX")
        if input_year and input_month and 2000 < input_year <= 2023 and 0 < input_month <= 12:
            _sql = provider.get('query4.sql', input_year=input_year, input_month=input_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) == 0:
                return render_template('not_found.html', error='Ошибка, ничего не найдено!')
            return render_template('db_result.html', schema=["id зала", 'Название зала', 'Количество сеансов'], result=product_result, query_numb="Query4")
        else:
            return render_template('not_found.html', error="Параметры запроса не введены, или введены неверно! "
                                                           "Введите год в формате XXXX, месяц в формате XX")
    elif request.method == 'GET':
        return render_template('query.html', ph_title1="Введите год", ph_title2="Введите месяц", title_name='Query4')



































"""
                Тут чисто блупринт запросов
                Тут все просто 
                Первая функция для 1 запроса
                Вторая функция для 2
"""