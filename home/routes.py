# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from home import blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import current_user
# from multi_tenant.models import Tenant
# from multi_tenant.models import db
# from multi_tenant.new_one import simple_cache
from flask import current_app
from authentication.models import Users
from login_panel import db
from authentication.util import hash_pass
import sqlite3 as sql
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask_paginate import get_page_args, Pagination



database_path = '/home/saubhagyam/Downloads/my_new_project/user_data.db'

@blueprint.route('/index')
@login_required
def index():

    with sql.connect('/home/saubhagyam/Downloads/my_data.db') as user:

        month = datetime.datetime.now().strftime('%Y-%m')
        
        cursor = user.cursor()

        total_user = message_data('SELECT COUNT(DISTINCT user_contact) FROM message_data')

        cursor.execute('SELECT COUNT(DISTINCT order_id) FROM all_customer_shop')
        total_orders = cursor.fetchone()

        cursor.execute("SELECT PRINTF('%.2f', SUM(price)) as price FROM all_customer_shop")
        total_sales = cursor.fetchone()

        cursor.execute("SELECT COUNT(DISTINCT order_id) FROM all_customer_shop WHERE delivery_status='Pending'")
        pending_orders = cursor.fetchone()

        total_messages = message_data('SELECT COUNT(message) FROM message_data')

        cursor.execute('SELECT COUNT(DISTINCT order_id) FROM all_customer_shop WHERE date LIKE ?', ('%' + month + '%',))
        current_month_orders = cursor.fetchone() 
        
        return render_template('home/index.html', segment='index', total_users=total_user[0][0], \
                               total_orders=total_orders[0], total_sales=total_sales[0], pending_orders=pending_orders[0], \
                               current_month_orders=current_month_orders[0], total_messages=total_messages[0][0])



@blueprint.route('/new_index')
@login_required
def new_index():

    return render_template('home/new_index.html', segment='index')
    

def message_data(data, messa_type=None, data_value=None):

    with sql.connect(database_path) as user:

        cursor = user.cursor()

        if messa_type == 'update_data':

            cursor.execute(data, data_value)
            user.commit()

        else:
            
            cursor.execute(data)
            data = cursor.fetchall()

            return data



def data_pagination(total_data, data_name, page_num=None):
    
    page, per_page, default_value = get_page_args(page_parameter='page', \
                                                  per_pageparameter='per_page')
    per_page = 10

    pagination = Pagination(page=page, per_page=per_page, record_name=data_name, \
                            total=total_data, css_framework='bootstrap4')

    if page_num is not None:

        page_num = int(page_num)
        page_num = page_num - 1
        new_page_num = str(page_num) + '0'

        return page, per_page, new_page_num, pagination
    
    else:

        return page, per_page, pagination




@blueprint.route('/<template>', methods=['POST', 'GET'])
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        global page_num
        global search_output
        
        page_num = request.args.get('page')
        search_output = request.args.get('search')
        date_data = request.args.get('date_input')
        categ_data = request.args.get('category')
        activate_status = request.args.get('activate_status')
        view_user = request.args.get('user_contact')
        user_details = request.args.get('user_details')
        user_messages = request.args.get('user_messages')
        user_messa_search = request.args.get('user_messa_search')
        user_del_status = request.args.get('user_delivery_status')
        order_search = request.args.get('order_search')
        message_search = request.args.get('message_search')
        search_value = request.args.get('search_value')
        delivered_status = request.args.get('delivered_status')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        email_update = request.args.get('email_update')

        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        print(categ_data)


        if segment == "users_data.html":

            with sql.connect('/home/saubhagyam/Downloads/user_data.db') as user:

                cursor = user.cursor()

                cursor.execute('SELECT COUNT(user_id) FROM message_data')

                total_users = cursor.fetchone()
                
                
                if search_output is not None:
                    
                    if page_num is not None:        
                        
                        cursor.execute('SELECT COUNT(*) FROM message_data WHERE user_name LIKE ?', ('%' + search_output + '%',))

                        total_user = cursor.fetchone()
                        
                        page, per_page, new_page_num, pagination = data_pagination(total_user[0], 'My Data', page_num)

                        cursor.execute('SELECT * FROM message_data WHERE \
                                       user_name LIKE ? LIMIT 10 OFFSET ?', \
                                       ('%' + search_output + '%', new_page_num,))

                        data = cursor.fetchall()
                        
                        return render_template("home/" + template, segment=segment, my_data=data,
                                               page=page, per_page=per_page, all_page=pagination)
                        
                    else:
                        
                        cursor.execute('SELECT COUNT(*) FROM message_data WHERE user_name LIKE ?', ('%' + search_output + '%',))
                        
                        total_user = cursor.fetchone()
                        
                        page, per_page, pagination = data_pagination(total_user[0], 'My Data')
                        
                        cursor.execute('SELECT * FROM message_data WHERE user_name LIKE ? LIMIT 10', ('%' + search_output + '%',))
                        
                        data = cursor.fetchall()
                        
                        return render_template("home/" + template, segment=segment, my_data=data,
                                               page=page, per_page=per_page, all_page=pagination)

                
                elif page_num is not None:
                    
                    page, per_page, new_page_num, pagination = data_pagination(total_users[0], 'My Data', page_num)
                    
                    cursor.execute('SELECT * FROM message_data LIMIT 10 OFFSET ?', (new_page_num,))
                    
                    data = cursor.fetchall()
                    
                    return render_template("home/" + template, segment=segment, my_data=data,
                                           page=page, per_page=per_page, all_page=pagination)
                
                else:
                    
                    page, per_page, pagination = data_pagination(total_users[0], 'My Data')

                    cursor.execute('SELECT * FROM message_data LIMIT 10')

                    data = cursor.fetchall()

                    return render_template("home/" + template, segment=segment, my_data=data,
                                           page=page, per_page=per_page, all_page=pagination)
            
                
        elif new_password is not None:

            if new_password == confirm_password:

                new_one = hash_pass(new_password)

                user = Users.query.get(current_user.id)
                user.password = new_one

                success_message = 'You have changed your password'

                db.session.commit()

                return render_template("home/change_password.html", segment=segment, success_message=success_message)

            else:

                message = 'Password is not Matched'

                return render_template("home/change_password.html", segment=segment, message=message)
        
        elif first_name and email_update is not None:

            user = Users.query.get(current_user.id)
            user.username = first_name
            user.firstname = first_name
            user.lastname = None
            user.email = email_update

            db.session.commit()

            return render_template("home/profile.html", segment=segment, email_user=current_user.email, \
                                   first_name=current_user.firstname, last_name=current_user.lastname)
        
        
        elif first_name and last_name and email_update is not None:

            user = Users.query.get(current_user.id)
            user.username = first_name + " " + last_name
            user.firstname = first_name
            user.lastname = last_name
            user.email = email_update

            db.session.commit()

            return render_template("home/profile.html", segment=segment, email_user=current_user.email, \
                                   first_name=current_user.firstname, last_name=current_user.lastname)
        
        
        elif segment == 'profile.html':

            user = Users.query.get(current_user.id)

            return render_template("home/profile.html", segment=segment, email_user=current_user.email, \
                                   first_name=current_user.firstname, last_name=current_user.lastname)
        
        elif segment == "user_shop_data.html":

            page_num = request.args.get('page')
            
            with sql.connect('/home/saubhagyam/Downloads/my_data.db') as user:
                
                cursor = user.cursor()

                cursor.execute('SELECT COUNT(*) FROM all_customer_shop')

                total_users = cursor.fetchone()
                   
                
                if search_output is not None:

                    if page_num is not None:
                        
                        cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE user_name LIKE ? OR \
                                        user_contact LIKE ? OR date LIKE ? OR quantity LIKE ? OR price LIKE ? \
                                        OR delivery_status LIKE ? OR order_id LIKE ? OR product_id LIKE ? \
                                        OR payment_method LIKE ? OR product_name LIKE ?', \
                                        ('%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%',))
                        
                        total_user = cursor.fetchone()
                        
                        page, per_page, new_page_num, pagination = data_pagination(total_user[0], 'My Data', page_num)


                        cursor.execute('SELECT * FROM all_customer_shop WHERE user_name LIKE ? OR \
                                        user_contact LIKE ? OR date LIKE ? OR quantity LIKE ? OR price LIKE ? \
                                        OR delivery_status LIKE ? OR order_id LIKE ? OR product_id LIKE ? \
                                        OR payment_method LIKE ? OR product_name LIKE ? ORDER BY date DESC LIMIT 10 OFFSET ?', \
                                        ('%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%', new_page_num,))
                                            
                        data = cursor.fetchall()

                        return render_template("home/" + template, segment=segment, my_data=data,
                                               page=page, per_page=per_page, all_page=pagination)
                        
                    else:
                        
                        cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE user_name LIKE ? OR \
                                        user_contact LIKE ? OR date LIKE ? OR quantity LIKE ? OR price LIKE ? \
                                        OR delivery_status LIKE ? OR order_id LIKE ? OR product_id LIKE ? \
                                        OR payment_method LIKE ? OR product_name LIKE ?', \
                                        ('%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%',))

                        total_user = cursor.fetchone()

                        page, per_page, pagination = data_pagination(total_user[0], 'My Data')
                        
                        cursor.execute('SELECT * FROM all_customer_shop WHERE user_name LIKE ? OR \
                                        user_contact LIKE ? OR date LIKE ? OR quantity LIKE ? OR price LIKE ? \
                                        OR delivery_status LIKE ? OR order_id LIKE ? OR product_id LIKE ? \
                                        OR payment_method LIKE ? OR product_name LIKE ? ORDER BY date DESC LIMIT 10', \
                                        ('%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%', '%' + search_output + '%', '%' + search_output + '%', \
                                         '%' + search_output + '%',))

                        data = cursor.fetchall()

                        return render_template("home/" + template, segment=segment, my_data=data,
                                               page=page, per_page=per_page, all_page=pagination)
                        
                        
                elif date_data and categ_data is not None:

                    if page_num is not None:
                        
                        cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE \
                                       (date LIKE ?) AND (product_name LIKE ?)', \
                                        ('%' + date_data + '%', '%' + categ_data + '%',))
                        
                        total_user = cursor.fetchone()
                        
                        page, per_page, new_page_num, pagination = data_pagination(total_user[0], 'My Data', page_num)


                        cursor.execute('SELECT * FROM all_customer_shop WHERE \
                                       (date LIKE ?) AND (product_name LIKE ?) \
                                       LIMIT 10 OFFSET ?', ('%' + date_data + '%', \
                                                            '%' + categ_data + '%', \
                                                                new_page_num,))

                        data = cursor.fetchall()


                        return render_template("home/" + template, segment=segment, my_data=data,
                                               page=page, per_page=per_page, all_page=pagination, 
                                               categ_option=categ_data)
                        
                    else:

                        cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE \
                                       (date LIKE ?) AND (product_name LIKE ?)', \
                                        ('%' + date_data + '%', '%' + categ_data + '%',))

                        total_user = cursor.fetchone()

                        page, per_page, pagination = data_pagination(total_user[0], 'My Data')

                        cursor.execute('SELECT * FROM all_customer_shop WHERE \
                                       (date LIKE ?) AND (product_name LIKE ?) \
                                       LIMIT 10', ('%' + date_data + '%', \
                                                   '%' + categ_data + '%',))

                        data = cursor.fetchall()

                        return render_template("home/" + template, segment=segment, my_data=data,
                                               page=page, per_page=per_page, all_page=pagination, 
                                               categ_option=categ_data)
                
                elif categ_data is not None:
                    
                    if page_num is not None:
                        
                        cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE product_name LIKE ?', ('%' + categ_data + '%',))
                        
                        total_user = cursor.fetchone()
                        
                        page, per_page, new_page_num, pagination = data_pagination(total_user[0], 'My Data', page_num)


                        cursor.execute('SELECT * FROM all_customer_shop WHERE product_name LIKE ? LIMIT 10 OFFSET ?', ('%' + categ_data + '%', new_page_num,))

                        data = cursor.fetchall()


                        return render_template("home/" + template, segment=segment, my_data=data,
                                               page=page, per_page=per_page, all_page=pagination, 
                                               categ_option=categ_data)
                        
                    else:

                        cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE product_name LIKE ?', ('%' + categ_data + '%',))

                        total_user = cursor.fetchone()

                        page, per_page, pagination = data_pagination(total_user[0], 'My Data')

                        cursor.execute('SELECT * FROM all_customer_shop WHERE product_name LIKE ? LIMIT 10', ('%' + categ_data + '%',))

                        data = cursor.fetchall()

                        return render_template("home/" + template, segment=segment, my_data=data,
                                               page=page, per_page=per_page, all_page=pagination,
                                               categ_option=categ_data)
                    
                    
                elif date_data is not None:
                    
                    if page_num is not None:
                        
                        cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE date LIKE ?', ('%' + date_data + '%',))
                        
                        total_user = cursor.fetchone()
                        
                        page, per_page, new_page_num, pagination = data_pagination(total_user[0], 'My Data', page_num)


                        cursor.execute('SELECT * FROM all_customer_shop WHERE date LIKE ? LIMIT 10 OFFSET ?', ('%' + date_data + '%', new_page_num,))

                        data = cursor.fetchall()


                        return render_template("home/" + template, segment=segment, my_data=data,
                                               page=page, per_page=per_page, all_page=pagination)
                        
                    else:

                        cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE date LIKE ?', ('%' + date_data + '%',))

                        total_user = cursor.fetchone()

                        page, per_page, pagination = data_pagination(total_user[0], 'My Data')

                        cursor.execute('SELECT * FROM all_customer_shop WHERE date LIKE ? LIMIT 10', ('%' + date_data + '%',))

                        data = cursor.fetchall()

                        return render_template("home/" + template, segment=segment, my_data=data,
                                               page=page, per_page=per_page, all_page=pagination)
                        
                
                elif page_num is not None:

                    page, per_page, new_page_num, pagination = data_pagination(total_users[0], 'My Data', page_num)

                    cursor.execute('SELECT * FROM all_customer_shop ORDER BY date DESC LIMIT 10 OFFSET ?', (new_page_num,))

                    data = cursor.fetchall()

                    return render_template("home/" + template, segment=segment, my_data=data,
                                           page=page, per_page=per_page, all_page=pagination)
            
                
                elif activate_status is not None:

                    cursor.execute('UPDATE all_customer_shop SET delivery_status=? WHERE order_id=?', ('Delivered', activate_status))

                    user.commit()

                    cursor.execute('SELECT * FROM all_customer_shop ORDER BY date DESC LIMIT 10')

                    data = cursor.fetchall()

                    page, per_page, pagination = data_pagination(total_users[0], 'My Data')

                    return render_template("home/" + template, segment=segment, my_data=data,
                                           page=page, per_page=per_page, all_page=pagination)

                

                else:

                    cursor.execute('SELECT * FROM all_customer_shop ORDER BY date DESC LIMIT 10')

                    data = cursor.fetchall()

                    page, per_page, pagination = data_pagination(total_users[0], 'My Data')

                    return render_template("home/" + template, segment=segment, my_data=data,
                                           page=page, per_page=per_page, all_page=pagination)
        
        
        elif segment == "user_message_data.html":

            with sql.connect('/home/saubhagyam/Downloads/my_data.db') as user:

                cursor = user.cursor()

                if view_user is not None:

                    cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE user_contact=?', (view_user,))
                    total_of_user = cursor.fetchone()

                    page, per_page, order_pagination = data_pagination(total_of_user[0], 'User Data')
                    
                    user_name = message_data(f'SELECT user_name FROM message_data WHERE \
                                             user_contact={view_user} ORDER BY \
                                             time_of_message DESC LIMIT 1')

                    cursor.execute('SELECT * FROM all_customer_shop WHERE \
                                    user_contact=? ORDER BY date DESC LIMIT 10', \
                                    (view_user,))

                    all_shop_data = cursor.fetchall()
                    
                    messa_data = message_data(f'SELECT message, time_of_message FROM \
                                                message_data WHERE user_contact={view_user} ORDER BY \
                                                time_of_message DESC LIMIT 10')
                    
                    total_messa_user = message_data(f'SELECT COUNT(*) FROM message_data WHERE user_contact={view_user}')

                    page, per_page, user_pagination = data_pagination(total_messa_user[0][0], 'User Data')

                    return render_template("home/user_details.html", segment=segment, user_name=user_name[0][0], \
                                            user_contact=view_user, my_data=all_shop_data, new_messa_data=messa_data, 
                                            order_pagin=order_pagination, user_pagin=user_pagination)
                    
                
                elif user_messa_search is not None:

                    if page_num is not None:
                        
                        total_user = message_data(f"SELECT COUNT(DISTINCT user_name) FROM message_data WHERE \
                                                  user_name LIKE '%{user_messa_search}%' OR delivery_status LIKE \
                                                  '%{user_messa_search}%' OR time_of_message LIKE '%{user_messa_search}%' OR \
                                                  user_contact LIKE '%{user_messa_search}%'")
                        
                        page, per_page, new_page_num, pagination = data_pagination(total_user[0][0], 'My Data', page_num)


                        data = message_data(f"SELECT user_name, delivery_status, time_of_message, user_contact FROM \
                                            message_data WHERE user_name LIKE '%{user_messa_search}%' OR \
                                            delivery_status LIKE '%{user_messa_search}%' OR time_of_message LIKE \
                                            '%{user_messa_search}%' OR user_contact LIKE '%{user_messa_search}%' GROUP BY \
                                            user_name ORDER BY time_of_message DESC LIMIT 10 OFFSET {new_page_num}")

                        return render_template("home/" + template, segment=segment, users=data, \
                                               all_page=pagination)
                        
                    else:
                        
                        total_user = message_data(f"SELECT COUNT(DISTINCT user_name) FROM message_data WHERE \
                                                  user_name LIKE '%{user_messa_search}%' OR delivery_status LIKE \
                                                  '%{user_messa_search}%' OR time_of_message LIKE '%{user_messa_search}%' OR \
                                                  user_contact LIKE '%{user_messa_search}%'")
                    

                        page, per_page, pagination = data_pagination(total_user[0][0], 'My Data')

                        data = message_data(f"SELECT user_name, delivery_status, time_of_message, user_contact FROM \
                                            message_data WHERE user_name LIKE '%{user_messa_search}%' OR \
                                            delivery_status LIKE '%{user_messa_search}%' OR time_of_message LIKE \
                                            '%{user_messa_search}%' OR user_contact LIKE '%{user_messa_search}%' GROUP BY \
                                            user_name ORDER BY time_of_message DESC LIMIT 10")

                        return render_template("home/" + template, segment=segment, users=data, \
                                               all_page=pagination)
                    
                elif user_del_status is not None:

                    cursor.execute('UPDATE all_customer_shop SET delivery_status=? WHERE order_id=?', ('Delivered', user_del_status,))
                    user.commit()

                    cursor.execute('SELECT user_contact FROM all_customer_shop WHERE order_id=?', (user_del_status,))
                    user_contact = cursor.fetchone()

                    cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE user_contact=?', (user_contact[0],))
                    total_of_user = cursor.fetchone()

                    page, per_page, order_pagination = data_pagination(total_of_user[0], 'User Data')
                    
                    cursor.execute('SELECT user_name FROM all_customer_shop WHERE user_contact=?', (user_contact[0],))
                    
                    user_name = cursor.fetchone()

                    cursor.execute('SELECT * FROM all_customer_shop WHERE \
                                    user_contact=? ORDER BY date DESC LIMIT 10', \
                                    (user_contact[0],))

                    all_shop_data = cursor.fetchall()

                    message_data(f"UPDATE message_data SET delivery_status='Delivered' WHERE order_id=?", \
                                 messa_type='update_data', data_value=(user_del_status,))
                    
                    messa_data = message_data(f'SELECT message, time_of_message FROM \
                                                message_data WHERE user_contact={user_contact[0]} ORDER BY \
                                                time_of_message DESC LIMIT 10')
                    
                    total_messa_user = message_data(f'SELECT COUNT(*) FROM message_data WHERE user_contact={user_contact[0]}')

                    page, per_page, user_pagination = data_pagination(total_messa_user[0][0], 'User Data')

                    return render_template("home/user_details.html", segment=segment, user_name=user_name[0], \
                                            user_contact=user_contact[0], my_data=all_shop_data, new_messa_data=messa_data, 
                                            order_pagin=order_pagination, user_pagin=user_pagination)
                

                elif user_details is not None:
                    
                    user_name = message_data(f'SELECT user_name FROM message_data WHERE \
                                             user_contact={user_details} ORDER BY \
                                             time_of_message DESC LIMIT 1')

                    cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE user_contact=?', (user_details,))
                    total_user = cursor.fetchone()
                    
                    if page_num:
                        
                        page, per_page, new_page_num, order_pagination = data_pagination(total_user[0], \
                                                                                         'User Data', page_num)
                        
                        cursor.execute('SELECT * FROM all_customer_shop WHERE \
                                        user_contact=? ORDER BY date DESC LIMIT 10 OFFSET ?', \
                                        (user_details, new_page_num,))
                        
                        all_shop_data = cursor.fetchall()
                        
                        return render_template("home/user_order_manage.html", segment=segment, my_data=all_shop_data, \
                                               user_contact=user_details, user_name=user_name[0][0], all_page=order_pagination)
                    
                    else:
                        
                        page, per_page, order_pagination = data_pagination(total_user[0], 'User Data')
                        
                        cursor.execute('SELECT * FROM all_customer_shop WHERE \
                                        user_contact=? ORDER BY date DESC LIMIT 10', \
                                        (user_details,))
                        
                        all_shop_data = cursor.fetchall()
                        
                        return render_template("home/user_order_manage.html", segment=segment, my_data=all_shop_data, \
                                               user_contact=user_details, user_name=user_name[0][0], all_page=order_pagination)
                
                
                elif order_search is not None:

                    cursor.execute('SELECT user_name FROM all_customer_shop WHERE user_contact=?', (search_value,))
                    user_name = cursor.fetchone()
                    
                    if page_num:
                        
                        cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE user_contact=? AND \
                                        product_name LIKE ? OR quantity LIKE ? OR date LIKE ? OR \
                                        price LIKE ? OR payment_method LIKE ? OR order_id LIKE ? OR \
                                        delivery_status LIKE ?', \
                                            (search_value, '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%',))
                        
                        total_search = cursor.fetchone()
                        
                        page, per_page, new_page_num, order_pagination = data_pagination(total_search[0], \
                                                                                         'User Data', page_num)
                        
                        cursor.execute('SELECT * FROM all_customer_shop WHERE user_contact=? AND \
                                        product_name LIKE ? OR quantity LIKE ? OR date LIKE ? OR \
                                        price LIKE ? OR payment_method LIKE ? OR order_id LIKE ? OR \
                                        delivery_status LIKE ? ORDER BY date DESC LIMIT 10 OFFSET ?', \
                                            (search_value, '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%',  new_page_num,))
                        
                        all_shop_data = cursor.fetchall()
                        
                        return render_template("home/user_order_manage.html", segment=segment, my_data=all_shop_data, \
                                               user_contact=search_value, user_name=user_name[0], all_page=order_pagination)
                    
                    else:
                        
                        cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE user_contact=? AND \
                                        product_name LIKE ? OR quantity LIKE ? OR date LIKE ? OR \
                                        price LIKE ? OR payment_method LIKE ? OR order_id LIKE ? OR \
                                        delivery_status LIKE ?', \
                                            (search_value, '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%',))
                        
                        total_search = cursor.fetchone()
                        
                        page, per_page, order_pagination = data_pagination(total_search[0], 'User Data')
                        
                        cursor.execute('SELECT * FROM all_customer_shop WHERE user_contact=? AND \
                                        product_name LIKE ? OR quantity LIKE ? OR date LIKE ? OR \
                                        price LIKE ? OR payment_method LIKE ? OR order_id LIKE ? OR \
                                        delivery_status LIKE ? ORDER BY date DESC LIMIT 10', \
                                            (search_value, '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%', \
                                             '%' + order_search + '%', '%' + order_search + '%',))
                        
                        all_shop_data = cursor.fetchall()
                        
                        return render_template("home/user_order_manage.html", segment=segment, my_data=all_shop_data, \
                                               user_contact=search_value, user_name=user_name[0], all_page=order_pagination)
                        
                
                elif message_search is not None:

                    user_name = message_data(f'SELECT user_name FROM message_data WHERE user_contact={search_value}')
                    
                    if page_num:
                        
                        total_search = message_data(f"SELECT COUNT(*) FROM message_data WHERE user_contact={search_value} AND \
                                                    message LIKE '%{message_search}%' OR time_of_message LIKE '%{message_search}%'")
                        
                        
                        page, per_page, new_page_num, message_pagination = data_pagination(total_search[0][0], \
                                                                                         'User Data', page_num)
                        
                        searched_message = message_data(f"SELECT message, time_of_message FROM \
                                                        message_data WHERE user_contact={search_value} AND \
                                                        message LIKE '%{message_search}%' OR time_of_message LIKE \
                                                        '%{message_search}%' ORDER BY time_of_message DESC LIMIT 10 OFFSET \
                                                        {new_page_num}")
                        
                        
                        return render_template("home/user_messages.html", segment=segment, my_data=searched_message, \
                                               user_contact=search_value, user_name=user_name[0][0], all_page=message_pagination)
                    
                    else:
                        
                        total_search = message_data(f"SELECT COUNT(*) FROM message_data WHERE user_contact={search_value} AND \
                                                    message LIKE '%{message_search}%' OR time_of_message LIKE '%{message_search}%'")
                        
                        
                        page, per_page, message_pagination = data_pagination(total_search[0][0], 'User Data')
                        
                        searched_message = message_data(f"SELECT message, time_of_message FROM message_data WHERE \
                                                        user_contact={search_value} AND message LIKE '%{message_search}%' OR \
                                                        time_of_message LIKE '%{message_search}%' ORDER BY time_of_message DESC LIMIT 10")
                        
                        
                        return render_template("home/user_messages.html", segment=segment, my_data=searched_message, \
                                               user_contact=search_value, user_name=user_name[0][0], all_page=message_pagination)
                

                elif delivered_status is not None:

                    cursor.execute('UPDATE all_customer_shop SET delivery_status=? WHERE order_id=?', ('Delivered', delivered_status,))
                    user.commit()

                    cursor.execute('SELECT user_contact FROM all_customer_shop WHERE order_id=?', (delivered_status,))
                    user_contact = cursor.fetchone()

                    cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE user_contact=?', (user_contact[0],))
                    total_of_user = cursor.fetchone()

                    page, per_page, order_pagination = data_pagination(total_of_user[0], 'User Data')

                    user_name = message_data(f'SELECT user_name FROM message_data WHERE \
                                             user_contact={user_contact[0]} ORDER BY \
                                             time_of_message DESC LIMIT 1')

                    cursor.execute('SELECT * FROM all_customer_shop WHERE \
                                    user_contact=? ORDER BY date DESC LIMIT 10', \
                                    (user_contact[0],))

                    all_shop_data = cursor.fetchall()

                    message_data(f"UPDATE message_data SET delivery_status='Delivered' WHERE order_id=?", \
                                 messa_type='update_data', data_value=(delivered_status,))
                    

                    return render_template("home/user_order_manage.html", segment=segment, user_name=user_name[0][0], \
                                            user_contact=user_contact[0], my_data=all_shop_data, all_page=order_pagination)

                

                elif user_messages is not None:

                    user_name = message_data(f'SELECT user_name FROM message_data WHERE \
                                             user_contact={user_messages} ORDER BY \
                                             time_of_message DESC LIMIT 1')
                    
                    total_messa_user = message_data(f'SELECT COUNT(*) FROM message_data WHERE user_contact={user_messages}')
                    
                    if page_num:
                        
                        page, per_page, new_page_num, message_pagination = data_pagination(total_messa_user[0][0], \
                                                                                         'User Data', page_num)
                        
                        user_message_data = message_data(f'SELECT message, time_of_message FROM \
                                                         message_data WHERE user_contact={user_messages} LIMIT 10 OFFSET \
                                                        {new_page_num}')
                        
                        return render_template("home/user_messages.html", segment=segment, my_data=user_message_data, \
                                               user_contact=user_messages, user_name=user_name[0][0], all_page=message_pagination)
                    
                    else:

                        page_num, per_page, message_pagination = data_pagination(total_messa_user[0][0], 'User Data')

                        user_message_data = message_data(f'SELECT message, time_of_message FROM \
                                                         message_data WHERE user_contact={user_messages} ORDER BY \
                                                         time_of_message DESC LIMIT 10')
                        
                        return render_template("home/user_messages.html", segment=segment, my_data=user_message_data, 
                                               user_contact=user_messages, user_name=user_name[0][0], all_page=message_pagination)
                

                else:
                    
                    total_user = message_data('SELECT COUNT(DISTINCT user_contact) FROM message_data')

                    page, per_page, user_messa_pagination = data_pagination(total_user[0][0], 'User Data')
                    
                    user_data = message_data('SELECT user_name, delivery_status, time_of_message, \
                                             user_contact FROM message_data GROUP BY user_contact ORDER BY \
                                             MAX(time_of_message) DESC LIMIT 10')
                    
                    return render_template("home/" + template, segment=segment, users=user_data, \
                                           all_page=user_messa_pagination)
                
                
        elif segment == 'user_order_manage.html':
            
            with sql.connect('/home/saubhagyam/Downloads/my_data.db') as user:

                cursor = user.cursor()

                cursor.execute('SELECT COUNT(*) FROM all_customer_shop WHERE user_contact=?', (view_user,))
                total_order = cursor.fetchone()

                page, page_num, pagination = data_pagination(total_order, 'Order Data')

                cursor.execute('SELECT * FROM all_customer_shop WHERE user_contact=?', (view_user,))
                data = cursor.fetchall()

                return render_template("home/" + template, segment=segment, my_data=data, all_page=pagination)
        
        else:

            return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
