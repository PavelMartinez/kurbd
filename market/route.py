from flask import Blueprint, render_template, request, session, current_app, url_for
from werkzeug.utils import redirect
from database.sql_provider import SQLProvider
from database.connection import UseDatabase
import datetime
import os
from access import external_required
from database.operations import select, select_dict, insert, select_dict2, update
from cache.wrapper import fetch_from_cache
import numpy as np

blueprint_market = Blueprint('bp_market', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_market.route('/', methods=['GET', 'POST'])
@external_required
def order_index():
    db_config = current_app.config['db_config']
    cache_config = current_app.config['cache_config']
    cached_select = fetch_from_cache('all_items_cached', cache_config)(select_dict)
    if request.method == 'GET':
        sql = provider.get('product_list.sql', date_id=datetime.date.today())
        items = cached_select(db_config, sql)
        basket_items = session.get('basket', {})

        return render_template('product_list.html', items=items, basket=basket_items)
    else:
        action = request.form.get('action')

        if action == 'choose_seat':
            tt_id = request.form.get('tt_id')

            sql1 = provider.get('max_row.sql', tt_id=tt_id)
            max_row = select_dict2(db_config, sql1)[0][0]

            seats_id = []


            sql3 = provider.get('total_prices.sql', tt_id=tt_id)
            prises = select_dict2(db_config, sql3)

            sql6 = provider.get('get_free_seat.sql', tt_id=tt_id)
            free_or_not = select_dict2(db_config, sql6)
            print(free_or_not)


            counter = 0
            for i in range(max_row):
                sql2 = provider.get('max_col.sql', tt_id=tt_id, line_id=i+1)
                max_cow = select_dict2(db_config, sql2)[0][0]
                a = []

                for j in range(max_cow):
                    c = {
                        'seat_line': i+1,
                        'seat_number': j+1,
                        'price': prises[counter][0],
                        'flag': bool(free_or_not[counter][0])
                    }
                    a.append(c)

                    counter = counter+1
                seats_id.append(a)
            print(seats_id)


            return render_template('seats.html', seats_id=seats_id, tt_id=tt_id )
        if action == 'update_seat':
            print("lol")
            seat_line = request.form.get('seat_line')
            seat_number = request.form.get('seat_number')
            tt_id = request.form.get('tt_id')
            finally_price = request.form.get('price')
            print("seat_line : ", seat_line)
            print("seat_number : ", seat_number)
            print("tt_id : ", tt_id)
            print("price : ", finally_price)

            sql4 = provider.get('what_film_place.sql', tt_id=tt_id)
            item = select_dict(db_config, sql4)[0]
            print(item)
            print(item['Country'])

            sql5 = provider.get('get_ticket_id.sql', tt_id=tt_id, line_id=seat_line, number_id=seat_number)
            ticket_id = select_dict(db_config, sql5)[0]['idTicket']
            print("ticket_id", ticket_id)

            add_to_basket(tt_id, seat_line, seat_number, item, finally_price, ticket_id)



        return redirect(url_for('bp_market.order_index'))

def delete_from_basket(prod_id: str):
    curr_basket = session.get('basket', {})
    # print("curr_basket1 : ", curr_basket)
    curr_basket.pop(prod_id, 4000)
    curr_basket = session.get('basket', {})
    # print("curr_basket2 : ", curr_basket)
    return True

def add_to_basket(tt_id, seat_line, seat_number, item, price, ticket_id):
    curr_basket = session.get('basket', {})
    print("curr_basket:  ", curr_basket)

    if str(ticket_id) in curr_basket:
        print('Zanyato')
    else:
        print('good')
        curr_basket[str(ticket_id)] = {
            'Country': item['Country'],
            'Place_name': item['Place_name'],
            'film_price': price,
            'seat_line': seat_line,
            'seat_number': seat_number,
            'tt_id': tt_id
        }
        session['basket'] = curr_basket
        session.permanent = True
    print("curr_basket:  ", curr_basket)
    return True

@blueprint_market.route('/save_order', methods=['GET','POST'])
def save_order():
    user_id = session.get('user_id')
    print('user_id : ', user_id)
    current_basket = session.get('basket', {})
    flag = False
    db_config = current_app.config['db_config']

    for item in current_basket:
        print("item: ", item)
        sql1 = provider.get('insert_bron.sql', ticket_id=item, user_id=user_id)
        res = update(db_config, sql1)
        if res:
            flag = True

    if flag == True:
        session.pop('basket')
        return render_template('order_created.html')
    else:
        return 'Что-то пошло не так'


@blueprint_market.route('/clear-basket')
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_market.order_index'))
