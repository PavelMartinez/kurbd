from flask import *
from database.operations import select, call_proc
from access import login_required, group_required
from database.sql_provider import SQLProvider
import os
from database.connection import UseDatabase as DBConnection

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))



report_list = [
    {'rep_name':'Выручка с фильмов', 'rep_id':'1'},
    {'rep_name':'Выручка с залов', 'rep_id':'2'}
]


report_url = {
    '1': {'create_rep':'bp_report.create_rep1', 'view_rep':'bp_report.view_rep1'},
    '2': {'create_rep':'bp_report.create_rep2', 'view_rep':'bp_report.view_rep2'}
}


@blueprint_report.route('/', methods=['GET', 'POST'])
@group_required
def start_report():
    if request.method == 'GET':
        return render_template('menu_report.html', report_list=report_list)
    else:
        rep_id = request.form.get('rep_id')
        print('rep_id = ', rep_id)
        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        print('url_rep = ', url_rep)
        return redirect(url_for(url_rep))

@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
@group_required
def create_rep1():
    if request.method == 'GET':
        print("GET_create")
        return render_template('report_create.html', name_rep="выручке с фильма", title='Отчет 1')
    else:
        print(current_app.config['db_config'])
        print("POST_create")
        try:
            rep_month = int(request.form.get('input_month'))
            rep_year = int(request.form.get('input_year'))
        except ValueError:
            return render_template('error.html', error="Параметры отчёта введены неверно! "
                                                           "Введите год в формате XXXX, месяц в формате XX")
        print("Loading...")
        if rep_year and rep_month and 2000 < rep_year <= 2023 and 0 < rep_month <= 12:
            _sql = provider.get('check_rep1.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            print(product_result)
            if (product_result[0][0] > 0):
                return render_template('error.html', error="Такой отчёт уже существует")
            else:
                res = call_proc(current_app.config['db_config'], 'stonks_report', rep_year, rep_month)
                print('res=', res)
                return render_template('report_created.html', rep_month=rep_month, rep_year=rep_year, name_rep="выручке с фильма")
        else:
            return render_template('error.html', error="Вы допустили ошибку! "
                                                           "Введите год в формате XXXX, месяц в формате XX")


@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
@group_required
def view_rep1():
    if request.method == 'GET':
        return render_template('view_rep.html', name_rep='выручке с фильма')
    else:
        try:
            rep_month = int(request.form.get('input_month'))
            rep_year = int(request.form.get('input_year'))
        except ValueError:
            return render_template('error.html', error="Параметры запроса введены неверно! "
                                                           "Введите год в формате XXXX, месяц в формате XX")
        if rep_year and rep_month and 2000 < rep_year <= 2023 and 0 < rep_month <= 12:
            _sql = provider.get('rep1.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if product_result:
                return render_template('result_rep1.html', schema=schema, result=product_result, rep_month=rep_month, rep_year=rep_year)
            else:
                return render_template('error.html', error="Такой отчёт не был создан")
        else:
            return render_template('error.html', error="Вы допустили ошибку! "
                                                           "Введите год в формате XXXX, месяц в формате XX")

@blueprint_report.route('/create_rep2', methods=['GET', 'POST'])
@group_required
def create_rep2():
    if request.method == 'GET':
        print("GET_create")
        return render_template('report_create.html', name_rep="выручке с зала", title='Отчет 2')
    else:
        try:
            rep_month = int(request.form.get('input_month'))
            rep_year = int(request.form.get('input_year'))
        except ValueError:
            return render_template('error.html', error="Параметры запроса введены неверно! "
                                                           "Введите год в формате XXXX, месяц в формате XX")
        if rep_year and rep_month and 2000 < rep_year <= 2023 and 0 < rep_month <= 12:
            _sql = provider.get('check_rep2.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            print(product_result)
            if (product_result[0][0] > 0):
                return render_template('error.html', error="Такой отчёт уже существует")
            else:
                res = call_proc(current_app.config['db_config'], 'places_report', rep_year, rep_month)
                print('res=', res)
                return render_template('report_created.html', rep_month=rep_month, rep_year=rep_year, name_rep="выручке с зала")
        else:
            return render_template('error.html', error="Вы допустили ошибку! "
                                                           "Введите год в формате XXXX, месяц в формате XX")

@blueprint_report.route('/view_rep2', methods=['GET', 'POST'])
@group_required
def view_rep2():
    if request.method == 'GET':
        return render_template('view_rep.html', name_rep="выручке с зала")
    else:
        try:
            rep_month = int(request.form.get('input_month'))
            rep_year = int(request.form.get('input_year'))
        except ValueError:
            return render_template('error.html', error="Параметры запроса введены неверно! "
                                                           "Введите год в формате XXXX, месяц в формате XX")
        if rep_year and rep_month and 2000 < rep_year <= 2023 and 0 < rep_month <= 12:
            _sql = provider.get('rep2.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if product_result:
                return render_template('result_rep1.html', schema=schema, result=product_result, rep_month=rep_month, rep_year=rep_year)
            else:
                return render_template('error.html', error="Такой отчёт не был создан")
        else:
            return render_template('error.html', error="Вы допустили ошибку! "
                                                           "Введите год в формате XXXX, месяц в формате XX")







































"""
                    Данный блупринт нужен чтобы создавать и просматривать отчеты
                    start_report - начальная страничка где можно выбрать какой отчет и что с ним сделать
                    остальные функции по названию можно понять что делают
                    !!!Важно!!!
                    Обратить внимание стоит на то как мы задаем информацию об этих отчетах
                    она хранится в строках 13-16 и 19-22
                    Мы написали словарик где ключом идет выбор функции чо нам сделать с отчетом а значением адресс этой функции в блупринте
"""