from flask import Blueprint, render_template, request, session, current_app, url_for, flash
from werkzeug.utils import redirect
from database.sql_provider import SQLProvider
from database.connection import UseDatabase
import os
from access import group_required
from database.operations import select, select_dict, insert, update

blueprint_edit = Blueprint('bp_edit', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_edit.route('/', methods=['GET'])
@group_required
def show_all_products():
    _sql = provider.get('all_products.sql')
    products = select_dict(current_app.config['db_config'], _sql)
    return render_template('all_products.html', products=products)

@blueprint_edit.route('/', methods=['POST'])
@group_required
def edit_product():
    action = request.form.get('action')
    prod_id = request.form.get('prod_id')
    if action == 'edit_prod':
        _sql = provider.get('get_product_by_id.sql', prod_id=prod_id)
        product = select_dict(current_app.config['db_config'], _sql)[0]
        print(product)
        return render_template('product_update.html', product=product)
    if action == 'del_prod':
        message = del_prod(prod_id)
        print(message)
        return render_template('update_ok.html', message=message)
    if action == 'update_prod':
        message = update_prod(prod_id)
        print(message)
        return render_template('update_ok.html', message=message)

def update_prod(prod_id):
    prod_name = request.form.get('prod_name')
    prod_price = request.form.get('prod_price')
    prod_measure = request.form.get('prod_measure')
    prod_study = request.form.get('prod_study')
    prod_lenght = request.form.get('prod_lenght')
    _sql = provider.get('update_product.sql', prod_name=prod_name, prod_measure=prod_measure, prod_price=prod_price,
                        prod_id=prod_id, prod_study=prod_study, prod_lenght=prod_lenght)
    result = update(current_app.config['db_config'], _sql)
    print('prod_name in update = ', prod_name)
    print('result = ', result)
    message = f'Фильм {prod_name} изменен в базе данных'
    return message


def del_prod(prod_id):
    _sql = provider.get('delete_product.sql', prod_id=prod_id)
    result = insert(current_app.config['db_config'], _sql)
    print("result3 = ", result)
    message = 'Упс! Что-то не так!'
    if result:
        message = 'Фильм удален из базы данных'
    return message

@blueprint_edit.route('/insert_prod', methods=['GET', 'POST'])
@group_required
def insert_prod():
    if request.method == 'POST':
        prod_name = request.form.get('prod_name')
        prod_price = request.form.get('prod_price')
        prod_measure = request.form.get('prod_measure')
        prod_study = request.form.get('prod_study')
        prod_lenght = request.form.get('prod_lenght')
        if not prod_name:
            flash("Вы не ввели название фильма!")
        if not prod_price:
            flash("Вы не ввели режиссера!")
        if not prod_measure:
            flash("Вы не ввели год выпуска фильма!")
        if prod_name and prod_price and prod_measure:
            _sql = provider.get('insert_product.sql', prod_name=prod_name, prod_price=prod_price,
                                prod_measure=prod_measure, prod_study=prod_study, prod_lenght=prod_lenght)
            result = insert(current_app.config['db_config'], _sql)
            print('result2 = ', result)
            message = 'Упс! Что-то не так!'
            if result:
                message = f'Фильм {prod_name} добавлен в базу данных'
            return render_template('update_ok.html', message=message)
    return render_template('product_update.html', product={})


































"""
        Блупринтик делает возможным редактирование информации о фильмах
        Добавить новый фильм, удалить, редактировать, все это делается тут
        show_all_products - тупо выводим все фильммы которые есть у нас сейчас и еще выводим кнопки для редактирования удаления и добавления
        edit_product - как некая функция распределения задач - если тебе нужно редактировать фильм, эта функция отправить тебя в функцию редактирования, если удалить, то в удаление
        Собственно по названиям остальных функций можно понять что они делают
"""
