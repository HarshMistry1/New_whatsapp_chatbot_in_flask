import json
from flask import Flask, request, render_template
from flask.json import jsonify
import sqlite3 as sql
import requests
import datetime
# from weasyprint import HTML
import pdfkit
from python_whatsapp_bot import Whatsapp, Inline_keyboard

# 919998978397

app = Flask(__name__)



with open('/home/Harsh159/chat_dir/config.json') as f:
    config = json.load(f)


app.config.update(config)


whatsapp_token = app.config["ACCESS_TOKEN"]
test_phone_num = app.config["PHONE_NUMBER_ID"]
verify_token = app.config["VERIFY_TOKEN"]
wa_num = app.config["RECIPIENT_WAID"]

# test_phone_num = '119306844496484'


wa_bot = Whatsapp(test_phone_num, whatsapp_token)



url = "https://graph.facebook.com/v17.0/" + test_phone_num + "/messages"

headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json",
        }



@app.route("/")
def main():
    return "The main page is on"



@app.route("/user-messages")
def user_message_data():
    connect = sql.connect("/home/Harsh159/chat_dir/user_data.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM message_data")

    data = cursor.fetchall()

    return render_template("user_message.html", data=data)


@app.route("/user_shop")
def user_shop_data():
    connect = sql.connect("/home/Harsh159/chat_dir/test_database/my_data.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM all_customer_shop")

    data = cursor.fetchall()

    return render_template("user_data.html", data=data)



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



def message_data(user_name, message, user_id, user_contact_num):

    with sql.connect("/home/Harsh159/chat_dir/user_data.db") as user:
        cursor = user.cursor()

        cursor.execute("INSERT INTO message_data (user_name, message, user_contact_num, user_id) VALUES (?, ?, ?, ?)",
        (user_name, message, user_contact_num, user_id))

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

    with sql.connect('/home/Harsh159/chat_dir/test_database/user_data.db') as user:

        cursor = user.cursor()

        cursor.execute('SELECT complaint FROM customer_complaints WHERE complaint_id=?', (id_message,))

        main_message  = cursor.fetchone()


        if main_message is not None:

            send_interactive_message(user_contact=from_num, message_type='button', \
                                     text_body=f'Thank you the response for {main_message[0]}. We will let you know within 3 days.', \
                                     button_messages=[(359, 'Complaint Section'), (809, 'Main Menu')])



        elif id_message == "1":
            wa_bot.send_message(from_num,
            "In AI/ML Development we create chatbot such as whatsapp chatbot.")

        elif id_message == "2":
            wa_bot.send_message(from_num,
            "We develop mobile application on high level.")

        elif id_message == "3":
            wa_bot.send_message(from_num,
            "We create website as your need.")

        elif id_message == "4":
            wa_bot.send_message(from_num,
            "We can let you integrate the chatbot as your need.")

        elif id_message == "5":
            wa_bot.send_message(from_num,
            "We have digital and social media marketing as your need.")




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
        return all_products_message(from_num)

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





def all_products_message(user_contact):

    with sql.connect('/home/Harsh159/chat_dir/test_database/user_data.db') as user:

        cursor = user.cursor()


        cursor.execute('SELECT product_id FROM main_product_list WHERE \
                        product_categ_id=?', (2,))

        caps_data = cursor.fetchall()


        cursor.execute('SELECT product_id FROM main_product_list WHERE \
                        product_categ_id=?', (1,))

        t_shirt_data = cursor.fetchall()


        cursor.execute('SELECT product_id FROM main_product_list WHERE \
                        product_categ_id=?', (3,))

        suit_data = cursor.fetchall()


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
                        "text": "Products for Men"
                        },
                    "body":{
                    "text": "Please select the option"
                    },
                    "action":{
                        "catalog_id": "655590996438757",
                        "sections": [
                            {
                                "title": "Caps for Men",
                                "product_items": [{"product_retailer_id": product_id[0]} \
                                                  for product_id in caps_data]
                            },
                            {
                                "title": "Suits for Men",
                                "product_items": [{"product_retailer_id": product_id[0]} \
                                                  for product_id in suit_data]
                            },

                            {
                                "title": "T-Shirts for Men",
                                "product_items": [{"product_retailer_id": product_id[0]} \
                                                  for product_id in t_shirt_data]

                            }

                        ]

                    }

                }
            }

    response = requests.post(url, json=data, headers=headers)
    print(f"Whatsapp message response :- {response.json}")
    response.raise_for_status()

    return response




def payment_text_message(text_body, from_num):

    send_interactive_message(user_contact=from_num, message_type='button', \
                             text_body=text_body, button_messages=[\
                             (409, 'Make Payment'), (809, 'Main Menu')])



def document_message(button_id_1, title_1, button_id_2, title_2, from_num, text_body, link, file_name):

    new_link = link + file_name

    data = {
        "messaging_product": "whatsapp",
        "to": from_num,
        "recipient_type": "individual",
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header":{
                "type": "document",
                "document":{
                    "filename": file_name,
                    "link": new_link
                    }
                },
                "body": {
                    "text": text_body
                    },
                "action": {
                    "buttons": [
                        {
                            "type": 'reply',
                            "reply": {
                                "id": button_id_1,
                                "title": title_1
                                }
                        },
                        {
                            "type": 'reply',
                            "reply": {
                                "id": button_id_2,
                                "title": title_2
                                }
                        }
                    ]
                }
            }
        }

    response = requests.post(url, json=data, headers=headers)
    print(f"Whatsapp message response :- {response.json}")
    response.raise_for_status()

    return response



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

    with sql.connect('/home/Harsh159/chat_dir/test_database/user_data.db') as user:

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




def generate_bill(from_num, payment_meth):


    date  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    with sql.connect('/home/Harsh159/chat_dir/test_database/my_data.db') as file:

        cursor = file.cursor()

        cursor.execute('SELECT product_name, quantity, price FROM main_cart_list WHERE \
                        user_contact=?', (from_num,))

        data = cursor.fetchall()

        document_link = 'https://www.pythonanywhere.com/user/Harsh159/files/home/Harsh159/chat_dir/public/assets/'


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


        for main_one in bill_data:

            cursor.execute('INSERT INTO all_customer_shop (user_name, user_contact, \
                            product_name, quantity, price, payment_method, date) VALUES \
                            (?, ?, ?, ?, ?, ?, ?)', (main_one[0], main_one[1], \
                            main_one[2], main_one[3], main_one[4], payment_meth, \
                            date))


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

        print(main_file_name)



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

                new_link = document_link + new_file_name


                pdfkit.from_string(rendered, f"/home/Harsh159/chat_dir/public/assets/{new_file_name}")


                if payment_meth == 'COD':


                    send_interactive_message(user_contact=from_num, message_type='button', \
                                             text_body='Your order will be delivered.', \
                                             header='document', button_messages=[(305, 'Shop Again'), \
                                             (809, 'Main Menu')], link=new_link, file_name=new_file_name)

                    cursor.execute('DELETE FROM main_cart_list')

                    file.commit()

                else:

                    send_interactive_message(user_contact=from_num, message_type='button', \
                                             text_body='Thank you for online payment', \
                                             header='document', button_messages=[(305, 'Shop Again'), \
                                             (809, 'Main Menu')], link=new_link, file_name=new_file_name)

                    cursor.execute('DELETE FROM main_cart_list')

                    file.commit()

            else:

                new_file_name = new_one + "_" + "1" + ".pdf"

                cursor.execute("INSERT INTO file_management (user_name, user_contact, \
                                file_name, date) VALUES (?, ?, ?, ?)", (customer_name[0], \
                                from_num, new_file_name, file_date))

                file.commit()

                new_link = document_link + new_file_name

                pdfkit.from_string(rendered, f"/home/Harsh159/chat_dir/public/assets/{new_file_name}")


                if payment_meth == 'COD':

                    send_interactive_message(user_contact=from_num, message_type='button', \
                                             text_body='Your order will be delivered.', \
                                             header='document', button_messages=[(305, 'Shop Again'), \
                                             (809, 'Main Menu')], link=new_link, file_name=new_file_name)

                    cursor.execute('DELETE FROM main_cart_list')

                    file.commit()

                else:

                    send_interactive_message(user_contact=from_num, message_type='button', \
                                             text_body='Thank you for online payment.', \
                                             header='document', button_messages=[(305, 'Shop Again'), \
                                             (809, 'Main Menu')], link=new_link, file_name=new_file_name)


                    cursor.execute('DELETE FROM main_cart_list')

                    file.commit()

        else:

            cursor.execute("INSERT INTO file_management (user_name, user_contact, \
                           file_name, date) VALUES (?, ?, ?, ?)", (customer_name[0], \
                           from_num, one_file_name, file_date))

            file.commit()

            new_link = document_link + one_file_name

            pdfkit.from_string(rendered, f"/home/Harsh159/chat_dir/public/assets/{one_file_name}")


            if payment_meth == 'COD':

                send_interactive_message(user_contact=from_num, message_type='button', \
                                         text_body='Your order will be delivered.', \
                                         header='document', button_messages=[(305, 'Shop Again'), \
                                         (809, 'Main Menu')], link=new_link, file_name=new_file_name)


                cursor.execute('DELETE FROM main_cart_list')

                file.commit()


            else:

                send_interactive_message(user_contact=from_num, message_type='button', \
                                         text_body='Your order will be delivered.', \
                                         header='document', button_messages=[(305, 'Shop Again'), \
                                         (809, 'Main Menu')], link=new_link, file_name=new_file_name)


                cursor.execute('DELETE FROM main_cart_list')

                file.commit()







def handle_whatsapp_message(body):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    user_name = body['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
    user_id = body['entry'][0]['id']
    user_contact_num = body['entry'][0]['changes'][0]['value']['messages'][0]['from']
    # current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    if message["type"] == "interactive":


        # List reply response

        if message["interactive"]["type"] == "list_reply":

            id_message = message["interactive"]["list_reply"]["id"]
            list_reply_message = message["interactive"]["list_reply"]["title"]

            message_data(user_name, list_reply_message, user_contact_num, user_id)

            return list_message(id_message, wa_num)



        # Button reply response

        elif message["interactive"]["type"] == "button_reply":

            message_body = message["interactive"]["button_reply"]["title"]
            id_message = message["interactive"]["button_reply"]["id"]

            message_data(user_name, message_body, user_contact_num, user_id)


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



    # Order Message

    elif message["type"] == "order":

        product_items = body["entry"][0]["changes"][0]["value"]\
                        ["messages"][0]["order"]["product_items"]

        with sql.connect('/home/Harsh159/chat_dir/test_database/my_data.db') as user:

            cursor = user.cursor()
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


            for products in product_items:


                cursor.execute('SELECT product_name FROM main_product_list WHERE \
                                product_id=?', (products['product_retailer_id'],))

                product_name = cursor.fetchone()


                cursor.execute('INSERT INTO main_cart_list (user_name, \
                                user_contact, product_name, product_id, \
                                quantity, price, date) VALUES (?, ?, ?, \
                                ?, ?, ?, ?)', (user_name, user_contact_num, \
                                product_name[0], products['product_retailer_id'], products['quantity'], \
                                products['item_price'], date))


                user.commit()


        payment_method(user_contact_num)




    elif message["type"] == "text":
        message_body = message["text"]["body"].lower()
        # We can convert in uppercase or in high.


        start_messages = ["hey", "hi", "hello"]


        if any([a in message_body for a in start_messages]):

            with sql.connect('/home/Harsh159/chat_dir/user_data.db') as user:
                cursor = user.cursor()

                cursor.execute('SELECT * FROM registered_users WHERE user_contact=?', (user_contact_num,))

                data = cursor.fetchone()

                if data is None:
                    message_data(user_name, message_body, user_contact_num, user_id)
                    return user_registration(user_contact_num)

                else:
                    message_data(user_name, message_body, user_contact_num, user_id)
                    return welcome_whatsapp_message(wa_num)


        else:

            text_message(user_contact_num, "Please start conversation with 'Hello'.")






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


if __name__ == "__main__":
   app.run(port=9000)
