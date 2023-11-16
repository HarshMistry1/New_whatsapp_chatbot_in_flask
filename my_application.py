import json
from flask import Flask, request, render_template
from flask.json import jsonify
import sqlite3 as sql
import requests
import datetime
import pdfkit
import random
from flask import send_file, send_from_directory
from python_whatsapp_bot import Whatsapp, Inline_keyboard
import os
from flask_migrate import Migrate
from flask_minify  import Minify
from sys import exit
from panel_config import config_dict
from login_panel import db, create_app
from string import ascii_uppercase, digits
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
from flask import abort
# from multi_tenant.models import db
# from multi_tenant.multi_database_management import get_tenant_session
# from multi_tenant.models import User
import pandas as pd
import razorpay

man = razorpay.Client(auth=("rzp_test_lrU6iwIvDYnbOO", "DsehDWPamICKR7VUJrTQ8PqN"))


new_data = pd.read_excel('/home/saubhagyam/Downloads/my_new_products.xlsx')

# 919998978397

app = Flask(__name__)

# app.secret_key = os.urandom(42)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:pwd@localhost/General?charset=utf8'
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
# app.config['SQLALCHEMY_BINDS'] = {
                # 'users': 'sqlite:///' + os.path.join(basedir, 'db.sqlite3'),
                # 'new': 'sqlite:///' + os.path.join(basedir, 'new_data.sqlite3')
                # }
# db.init_app(app)


@app.route("/<tenant_name>/users")
def index(tenant_name):
    tenant_session = get_tenant_session(tenant_name)
    if not tenant_session:
        abort(404)
    users = tenant_session.query(User).all()
    return jsonify({tenant_name: [i.username for i in users]})

with open('/home/saubhagyam/Downloads/my_new_project/config.json') as f:
    config = json.load(f)


app.config.update(config)


whatsapp_token = app.config["ACCESS_TOKEN"]
test_phone_num = app.config["PHONE_NUMBER_ID"]
verify_token = app.config["VERIFY_TOKEN"]
wa_num = app.config["RECIPIENT_WAID"]

test_phone_num = '119306844496484'


wa_bot = Whatsapp(test_phone_num, whatsapp_token)



url = "https://graph.facebook.com/v17.0/" + test_phone_num + "/messages"

headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json",
        }



@app.route("/")
def main():
    return render_template("accounts/login.html")


def send_interactive_message(user_contact, message_type, text_body, header=None, header_text=None, file_name=None, link=None, button_messages=None, list_data=None):

    data = {
        "messaging_product": "whatsapp",
        "to": user_contact,
        "recipient_type": "individual",
        "type": "interactive",
        "interactive": {
            "type": message_type,
            "body": {
                "text": text_body

                }
            }
        }

    if header:

        if header == 'text':
            data['interactive']['header'] = {'type': header, \
                                              f'{header}': header_text}

        elif header in ['document', 'video', 'image']:

            data['interactive']['header'] = {'type': header, \
                                             f'{header}': {
                                             'filename': file_name,
                                             'link': link}}


    if message_type == 'list':

        data['interactive']['action'] = {'button': 'All Options', \
                                         'sections': [\
                                         {'title': 'All Options',
                                         'rows':[{'id': main_num,'title': title,
                                         'description': information} for main_num, \
                                         title, information in list_data]}]}

    elif message_type == 'button':

        data['interactive']['action'] = {'buttons': [{'type': 'reply', \
                                         'reply': {'id': main, \
                                         'title': message}} for main, message in button_messages]}
    
    elif message_type == 'address_message':
        data['interactive']['action'] = {
                   "name": "address_message",
                   "parameters": {
                      "country" :"IN"
                   }
              }




    response = requests.post(url, json=data, headers=headers)
    print(f"Whatsapp message response :- {response.json}")
    response.raise_for_status()

    return response



def welcome_whatsapp_message(from_num):
    my_data = request.get_json()
    user_name = my_data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']

    text_message(from_num, f"Hello {user_name}.")

    text_message(from_num, "Welcome to Saubhagyam Web Pvt. Ltd.")


    send_interactive_message(user_contact=from_num, message_type='button',
                             text_body='Please select the option', \
                             button_messages=[(135, 'Shop Now'), \
                             (136, 'Contact Saubhagyam'), (137, 'FAQ')])



def message_data(user_name, message, user_id, time_of_message, user_contact_num, order_id=None, delivery_status=None):

    with sql.connect("/home/saubhagyam/Downloads/my_new_project/user_data.db") as user:
        cursor = user.cursor()

        if delivery_status:

            cursor.execute("INSERT INTO message_data (user_name, message, user_num, user_contact, order_id, time_of_message, \
                           delivery_status) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_name, \
                           message, user_id, user_contact_num, order_id, time_of_message, delivery_status))

            user.commit()

        else:

            cursor.execute("INSERT INTO message_data (user_name, message, user_num, time_of_message, user_contact) VALUES (?, ?, ?, ?, ?)", \
                          (user_name, message, user_id, time_of_message, user_contact_num))

            user.commit()



def user_registration(from_num):

    wa_bot.send_message(from_num,
                        'Welcome to SAUBHAGYAM Pvt. Ltd. It looks like you need to create an account to see all services.',
                        reply_markup=Inline_keyboard(['Create an account', 'Contact Saubhagyam']))



def main_menu(from_num):

    send_interactive_message(user_contact=from_num, message_type='button', \
                             text_body='Please select the option', \
                             button_messages=[(135, 'Shop Now'), \
                             (136, 'Contact Saubhagyam'), (137, 'FAQ')])




def list_message(id_message, from_num):

    with sql.connect("/home/saubhagyam/Downloads/my_new_project/test_database/my_data.db") as user:

        cursor = user.cursor()

        cursor.execute('SELECT complaint FROM customer_complaints WHERE complaint_id=?', (id_message,))

        main_message  = cursor.fetchone()


        if main_message is not None:

            send_interactive_message(user_contact=from_num, message_type='button', \
                                     text_body=f'Thank you the response for {main_message[0]}. We will let you know within 3 days.', \
                                     button_messages=[(359, 'Complaint Section'), (809, 'Main Menu')])



        elif id_message == "101":
            all_products_message(from_num, 'All Products 1', 30)

        elif id_message == "102":
            all_products_message(from_num, 'All Products 2', 60, 30)

        elif id_message == "103":
            all_products_message(from_num, 'All Products 3', 90, 60)

        elif id_message == "104":
            all_products_message(from_num, 'All Products 4', 120, 90)

        elif id_message == "105":
            all_products_message(from_num, 'All Products 5', 150, 120)




def button_message(id_message, from_num=None):

    if id_message == "201":
        return cod_payment_method(user_contact=from_num)

    elif id_message == "301":
        return online_payment_method(user_contact=from_num)

    elif id_message == "359":
        return complaint_list_message(from_num)

    elif id_message == "409":
        return payment_method(from_num)

    elif id_message == "305" or id_message == "809":
        return main_menu(wa_num)




def interactive_message(message, from_num):

    if message == "Shop Now":
        new_one = [(101, 'All Products 1', 'In this one we have more products.'), \
                   (102, 'All Products 2', 'In this one we have new prodcuts.'), \
                   (103, 'All Products 3', 'In this one we will have more new products.'), \
                   (104, 'All Products 4', 'In this one we will have more new products.'), \
                   (105, 'All Products 5', 'In this one we will have more new products.')]
        
        send_interactive_message(user_contact=from_num, message_type='list', \
                                 text_body='Please select the option', \
                                 list_data=new_one)

    elif message == "Contact Saubhagyam":
        return complaint_list_message(from_num)

    elif message == "Main Menu":
        return main_menu(from_num)

    elif message == "FAQ":
        return faq_message(from_num)

    elif message == "Make Payment":
        return payment_method(from_num)

    elif message == "COD":
        return cod_payment_method(from_num)

    elif message == "Online Payment":
        return online_payment_method(from_num)

    elif message == "Customer Care":
        return customer_care_response(from_num)




def customer_care_response(from_num):
    wa_bot.send_message(from_num, text='Please talk to our customer care by this number')





def all_products_message(user_contact, message_title, end_num, start_num=None):

    with sql.connect("/home/saubhagyam/Downloads/my_new_project/user_data.db") as user:

        cursor = user.cursor()


        # cursor.execute('SELECT product_id FROM new_product_list WHERE \
                        # product_categ_id=?', (2,))

        # caps_data = cursor.fetchall()


        # cursor.execute('SELECT product_id FROM new_product_list WHERE \
                        # product_categ_id=?', (5,))

        # t_shirt_data = cursor.fetchall()


        # cursor.execute('SELECT product_id FROM new_product_list WHERE \
                        # product_categ_id=?', (1,))

        # suit_data = cursor.fetchall()


        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": user_contact,
            "type": "interactive",
            "interactive":
                {
                    "type": "product_list",
                    "header":{
                        "type": "text",
                        "text": "All Products"
                        },
                    "body":{
                    "text": "Please select the option"
                    },
                    "action":{
                        "catalog_id": "2323842411337155",
                        "sections": [
                            {
                                "title": message_title,
                                "product_items": [{"product_retailer_id": product_id} \
                                                  for product_id in new_data['id'][start_num:end_num]]
                            },
                            # {
                                # "title": "All Products 4",
                                # "product_items": [{"product_retailer_id": product_id} \
                                                  # for product_id in new_data['id'][91:120]]
                            # },
                            # {
                                # "title": "All Products 5",
                                # "product_items": [{"product_retailer_id": product_id} \
                                                  # for product_id in new_data['id'][121:150]]
                            # }
                            # {
                                # "title": "Suits for Men",
                                # "product_items": [{"product_retailer_id": product_id[0]} \
                                                  # for product_id in suit_data]
                            # },

                            # {
                                # "title": "T-Shirts for Men",
                                # "product_items": [{"product_retailer_id": product_id[0]} \
                                                  # for product_id in t_shirt_data]

                            # }

                        ]

                    }

                }
            }

    response = requests.post(url, json=data, headers=headers)
    print(f"Whatsapp message response :- {response.json}")
    response.raise_for_status()

    return response


def send_link_message(price, user_name, user_contact, address):

    new_num = '+' + user_contact
    
    new_one = man.payment_link.create({
        "amount": price*100,
        "currency": "INR",
        "accept_partial": True,
        "first_min_partial_amount": 100,
        "description": "For XYZ purpose",
        "customer": {
            "name": user_name,
            "contact": new_num
            },
        "notify": {
                "sms": True,
                "email": True,
                "whatsapp": True
                },
        "reminder_enable": True,
        "notes": {
            "address": address
            }
            })
    new_link = new_one['short_url']

    text_message(user_contact, f"Thank you for shop with us. \n Please make your payment here {new_link}.")



def payment_success_message(from_num, message):
    return text_message(from_num, message)



def payment_text_message(text_body, from_num):

    send_interactive_message(user_contact=from_num, message_type='button', \
                             text_body=text_body, button_messages=[\
                             (409, 'Make Payment'), (809, 'Main Menu')])




def cod_payment_method(user_contact):

    return generate_bill(user_contact, payment_meth='COD')




def online_payment_method(user_contact):

    return generate_bill(user_contact, payment_meth='Online Payment')




def templated_message(from_num, name):

    data = {
        "messaging_product": "whatsapp",
        "to": from_num,
        "type": "template",
        "template":
            {
                "name": name,
                "language":{
                    "code": "en_US"
                    }
            },
            "components":[{
                        "type": "header",
                        "parameters":[{
                            "type": "image",
                            "text": name
                            }
                        ]
                    }
                ]

        }
    response = requests.post(url, json=data, headers=headers)
    print(f"whatsapp message response: {response.json()}")
    response.raise_for_status()



def faq_message(from_num):

    text_message(from_num, "To make payment, you have shop first.")

    text_message(from_num, "You can get the product list at our website.")

    text_message(from_num, "You can get your bill at our website.")

    text_message(from_num, "You can see all products in cart list.")

    text_message(from_num, "You can check your profile at our website.")

    return send_interactive_message(user_contact=from_num, message_type='button', \
                                    text_body="Please check for more answers at our website.", \
                                    button_messages=[(305, "For Shop"), (809, "Main Menu")])




def text_message(from_num, text_body):

    data = {
        "messaging_product": "whatsapp",
        "to": from_num,
        "recipient_type": "individual",
        "type": "text",
        "text": {
            "body": text_body
            }
        }

    response = requests.post(url, json=data, headers=headers)
    print(f"Whatsapp message response :- {response.json}")
    response.raise_for_status()

    return response



def complaint_list_message(from_num):

    with sql.connect("/home/saubhagyam/Downloads/my_new_project/test_database/my_data.db") as user:

        cursor = user.cursor()

        cursor.execute('SELECT complaint_id, complaint, details FROM customer_complaints')


        complaints = cursor.fetchall()

        send_interactive_message(user_contact=from_num, message_type='list', \
                                 text_body='Please select the option', \
                                 list_data=complaints)




def payment_method(from_num):

    send_interactive_message(user_contact=from_num, message_type='button', \
                             text_body='How would you like to pay?', \
                             button_messages=[(201, 'COD'), (301, 'Online Payment')])



def random_numbers(len_of_num=6):

    main_num = digits + ascii_uppercase

    new_num = random.choices(main_num[:18], k=len_of_num)

    new_num = "".join(new_num)

    return new_num




def generate_bill(from_num, payment_meth, address):
    
    date  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with sql.connect('/home/saubhagyam/Downloads/my_new_project/test_database/my_data.db') as file:

        cursor = file.cursor()

        cursor.execute('SELECT product_name, quantity, price FROM main_cart_list WHERE \
                        user_contact=?', (from_num,))

        data = cursor.fetchall()

        document_link = "https://2c21-2401-4900-1f3f-388b-66e-903-c4b-d4c.ngrok-free.app/download"


        cursor.execute('SELECT SUM(quantity*price) as new_price \
                        FROM main_cart_list WHERE user_contact=?', \
                        (from_num,))


        price = cursor.fetchone()

        file_date = datetime.datetime.now().strftime('%Y-%m-%d')


        cursor.execute('SELECT user_name FROM registered_users WHERE \
                        contact_user=?', (from_num,))

        customer_name = cursor.fetchone()


        rendered = render_template('bill.html', data=data, total_price=price[0], \
                                    date=file_date, payment_meth=payment_meth)


        cursor.execute('SELECT user_name, user_contact, product_name, quantity, price \
                        FROM main_cart_list WHERE user_contact=?', (from_num,))


        bill_data = cursor.fetchall()


        new_num = random_numbers(6)

        main_path = "/home/saubhagyam/Downloads/my_new_project/public/assets/"


        for main_one in bill_data:

            cursor.execute('SELECT product_id FROM all_customer_shop \
                            ORDER BY product_id DESC LIMIT 1')

            product_id_num = cursor.fetchone()

            product_id_num = product_id_num[0] + 1

            cursor.execute('INSERT INTO all_customer_shop (user_name, user_contact, \
                            product_name, quantity, price, payment_method, date, \
                            order_id, product_id, shipping_address) VALUES \
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (main_one[0], \
                            main_one[1], main_one[2], main_one[3], \
                            main_one[4], payment_meth, date, new_num, \
                            product_id_num, address))


            file.commit()



        ano_name = customer_name[0].split(" ")
        new_name = "_".join(ano_name)

        new_one = new_name + "_" + file_date + "_" + "bill"

        one_file_name = new_one + ".pdf"


        cursor.execute("SELECT file_name FROM file_management WHERE \
                        user_contact=? and date=? ORDER BY \
                        file_name DESC LIMIT 1", (from_num, file_date,))

        # You can see the top data in Ascending order.


        main_file_name = cursor.fetchone()


        if main_file_name is not None:

            main_file_name = main_file_name[0].split(".")

            main_file_name = main_file_name[0]


            if main_file_name[-1].isdigit():

                big_one = int(main_file_name[-1]) + 1

                big_one = str(big_one)

                new_file_name = new_one + "_" + big_one + ".pdf"


                cursor.execute("INSERT INTO file_management (user_name, user_contact, \
                                file_name, date) VALUES (?, ?, ?, ?)", \
                                (customer_name[0], from_num, new_file_name, file_date))

                file.commit()

                file_path = os.path.join(main_path, new_file_name)
                print(file_path)
                
                pdfkit.from_string(rendered, file_path)

                file_download(file_path)

                send_interactive_message(user_contact=from_num, message_type='button', \
                                         text_body=f'Thank you for online payment by {payment_meth}', \
                                         header='document', button_messages=[(305, 'Shop Again'), \
                                         (809, 'Main Menu')], link=document_link, file_name=new_file_name)
                
                cursor.execute('DELETE FROM main_cart_list')
                
                file.commit()


            else:

                new_file_name = new_one + "_" + "1" + ".pdf"

                cursor.execute("INSERT INTO file_management (user_name, user_contact, \
                                file_name, date) VALUES (?, ?, ?, ?)", (customer_name[0], \
                                from_num, new_file_name, file_date))

                file.commit()
                
                file_path = os.path.join(main_path, new_file_name)
                print(file_path)

                pdfkit.from_string(rendered, file_path)

                file_download(file_path)
                
                send_interactive_message(user_contact=from_num, message_type='button', \
                                         text_body=f'Thank you for online payment by {payment_meth}', \
                                         header='document', button_messages=[(305, 'Shop Again'), \
                                         (809, 'Main Menu')], link=document_link, file_name=new_file_name)
                
                cursor.execute('DELETE FROM main_cart_list')
                
                file.commit()


                
        else:

            cursor.execute("INSERT INTO file_management (user_name, user_contact, \
                           file_name, date) VALUES (?, ?, ?, ?)", (customer_name[0], \
                           from_num, one_file_name, file_date))

            file.commit()
            
            file_path = os.path.join(main_path, one_file_name)
            print(file_path)
            
            pdfkit.from_string(rendered, file_path)
            
            file_download(file_path)

            send_interactive_message(user_contact=from_num, message_type='button', \
                                         text_body=f'Thank you for online payment by {payment_meth}', \
                                         header='document', button_messages=[(305, 'Shop Again'), \
                                         (809, 'Main Menu')], link=document_link, file_name=one_file_name)
            
            cursor.execute('DELETE FROM main_cart_list')
            
            file.commit()






def handle_whatsapp_message(body):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    user_name = body['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
    user_id = body['entry'][0]['id']
    user_contact_num = body['entry'][0]['changes'][0]['value']['messages'][0]['from']
    time_of_message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    if message["type"] == "interactive":


        # List reply response

        if message["interactive"]["type"] == "list_reply":

            id_message = message["interactive"]["list_reply"]["id"]
            list_reply_message = message["interactive"]["list_reply"]["title"]

            message_data(user_name, list_reply_message, user_id, time_of_message, user_contact_num)

            return list_message(id_message, user_contact_num)



        # Button reply response

        elif message["interactive"]["type"] == "button_reply":

            message_body = message["interactive"]["button_reply"]["title"]
            id_message = message["interactive"]["button_reply"]["id"]

            message_data(user_name, message_body, user_id, time_of_message, user_contact_num)

            if message_body == 'Shop Now':

                return interactive_message(message_body, user_contact_num)


            elif message_body == 'FAQ':

                return interactive_message(message_body, user_contact_num)


            elif message_body == 'Make Payment':

                return interactive_message(message_body, from_num=user_contact_num)


            elif message_body == 'COD':

                return interactive_message(message_body, from_num=user_contact_num)


            elif message_body == 'Online Payment':

                return interactive_message(message_body, from_num=user_contact_num)


            elif message_body == 'All Products':

                return interactive_message(message_body, from_num=user_contact_num)


            elif message_body == 'Contact Saubhagyam':

                return interactive_message(message_body, from_num=user_contact_num)

            else:

                return button_message(id_message, user_contact_num)
        
        elif message['interactive']['type'] == 'nfm_reply':
            
            address_data = eval(message['interactive']['nfm_reply']['response_json'])
            
            main_address_data = address_data["values"]["address"]

            with sql.connect('/home/saubhagyam/Downloads/my_new_project/test_database/my_data.db') as user:

                cursor = user.cursor()

                cursor.execute('SELECT SUM(quantity*price) as new_price \
                               FROM main_cart_list WHERE user_contact=?', \
                               (user_contact_num,))
                
                price = cursor.fetchone()
                
                send_link_message(price[0], user_name, user_contact_num, main_address_data)


    # Order Message

    elif message["type"] == "order":

        product_items = body["entry"][0]["changes"][0]["value"]\
                        ["messages"][0]["order"]["product_items"]

        # new_link = 'https://924c-2401-4900-1f3f-a73d-3d21-4de8-1183-e549.ngrok-free.app/download'

        # one_file_name = 'new_bill.pdf'

        # send_link_message(total_price, user_name, user_contact_num)

        # send_interactive_message(user_contact=user_contact_num, message_type='button', \
                                 # text_body='Your order will be delivered.', \
                                 # header='document', button_messages=[(305, 'Shop Again'), \
                                 # (809, 'Main Menu')], link=new_link, file_name=one_file_name)


        with sql.connect('/home/saubhagyam/Downloads/my_new_project/test_database/my_data.db') as user:

            cursor = user.cursor()
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


            for products in product_items:


                cursor.execute('SELECT title FROM new_product_list WHERE \
                               id=?', (products['product_retailer_id'],))

                product_name = cursor.fetchone()


                cursor.execute('INSERT INTO main_cart_list (user_name, \
                                user_contact, product_name, product_id, \
                                quantity, price, date) VALUES (?, ?, ?, \
                                ?, ?, ?, ?)', (user_name, user_contact_num, \
                                product_name[0], products['product_retailer_id'], products['quantity'], \
                                products['item_price'], date))


                user.commit()

                send_interactive_message(user_contact=user_contact_num, message_type='address_message', \
                                         text_body='Please enter your address, to continue payment.')


    elif message["type"] == "text":
        message_body = message["text"]["body"].lower()
        # We can convert in uppercase or in high.


        start_messages = ["hey", "hi", "hello"]


        if any([a in message_body for a in start_messages]):

            with sql.connect("/home/saubhagyam/Downloads/my_new_project/user_data.db") as user:
                cursor = user.cursor()

                cursor.execute('SELECT * FROM registered_users WHERE user_contact=?', (user_contact_num,))

                data = cursor.fetchone()

                if data is None:
                    message_data(user_name, message_body, user_id, time_of_message, user_contact_num)
                    return user_registration(user_contact_num)

                else:
                    message_data(user_name, message_body, user_id, time_of_message, user_contact_num)
                    return welcome_whatsapp_message(user_contact_num)
        else:

            max_len = 25
            
            path = '/home/saubhagyam/Downloads/my_new_project/'
            
            with open(path + 'new_intents.json', 'r') as f:
                data = json.loads(f.read())
            
            tokeniser_path = open(path + 'tokenizer.pkl', 'rb')
            tokeniser = pickle.load(tokeniser_path)
            
            label_path = open(path + 'label_encoder.pkl', 'rb')
            label_enc = pickle.load(label_path)
            
            model = tf.keras.models.load_model(path + 'new_chatbot_model.h5')
            
            res = model.predict(pad_sequences(tokeniser.texts_to_sequences([message_body]),
                                  truncating='post', maxlen=max_len))
            
            tag_out = label_enc.inverse_transform([np.argmax(res)])
            
            for p in data['intents']:
                if p['tag'] == tag_out:
                    message = np.random.choice(p['responses'])
                    text_message(user_contact_num, message)






def handle_message(request):
    # Parse Request body in json format
    body = request.get_json()
    print(f"request body: {body}")

    try:
        # info on WhatsApp text message payload:
        # https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
        if body.get("object"):
            if (
                body.get("entry")
                and body["entry"][0].get("changes")
                and body["entry"][0]["changes"][0].get("value")
                and body["entry"][0]["changes"][0]["value"].get("messages")
                and body["entry"][0]["changes"][0]["value"]["messages"][0]
            ):

                handle_whatsapp_message(body)
            return jsonify({"status": "ok"}), 200
        else:
            # if the request is not a WhatsApp API event, return an error
            return (
                jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
                404,
            )
    # catch all other errors and return an internal server error
    except Exception as e:
        print(f"unknown error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


DEBUG = (os.getenv('DEBUG', 'False') == 'True')


get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )


def webhook_message(request):
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == verify_token:
            print("Webhook worked")
            return challenge, 200
        else:
            print("Please check the webhook")
            return jsonify({"status": "error", "message": "Check the webhook"}), 403

    else:
        print("Please check the application")
        return jsonify({"status": "error", "message": "Check the application"}), 404


@app.route("/webhook", methods=["POST", "GET"])
def check_webhook():
    if request.method == "GET":
        return webhook_message(request)
    elif request.method == "POST":
        return handle_message(request)


@app.route("/payment_success", methods=["POST", "GET"])
def payment():
    if request.method == "GET":
        main = request.args.get('razorpay_payment_link_status')
        return main

    elif request.method == "POST":
        return "Payment is now."


@app.route("/new_webhook", methods=["POST", "GET"])
def new_webhook():
    if request.method == "GET":
        main = request.get_json()
        print(main)

    elif request.method == "POST":
        main = request.get_json()
        pay_method = main['payload']['payment']['entity']['method']
        print(main)
        user_contact = main['payload']['payment_link']['entity']['customer']['contact'].split("+")
        address = main['payload']['order']['entity']['notes']['address']

        generate_bill(user_contact[1], pay_method, address)
        # payment_success_message(user_contact[1], f'Thank you for the payment by {pay_method}.\nYou will get your products.')
        return main

@app.route("/download/<file_name>", methods=["POST", "GET"])
def file_download(file_name):
    path = '/home/saubhagyam/Downloads/my_new_project/public/assets/'
    new_path=os.path.join(path, file_name)
    return send_file(new_path, as_attachment=True)

# new_file_download('/home/saubhagyam/Downloads/my_new_project/public/assets/', "new_bill.pdf")

if __name__ == "__main__":
   app.run(port=3000, debug=True)
















































