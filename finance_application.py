import json
from flask import Flask, request, render_template
from flask.json import jsonify
import sqlite3 as sql
import requests
import datetime
# from weasyprint import HTML
# import pdfkit
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


wa_bot = Whatsapp(test_phone_num, whatsapp_token)



url = "https://graph.facebook.com/v17.0/" + test_phone_num + "/messages"

headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json",
        }



@app.route("/")
def main():
    return "The main page is on"



@app.route("/user_data")
def user_message_data():
    connect = sql.connect("/home/Harsh159/chat_dir/test_database/my_data.db", timeout=5)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM finance_data")

    data = cursor.fetchall()

    return render_template("user_message.html", data=data)



def welcome_whatsapp_message(from_num):
    my_data = request.get_json()
    user_name = my_data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']

    text_message(from_num, f"Hello {user_name}.")

    text_message(from_num, "Welcome to Shree Saraswati Finance Pvt. Ltd.")


    data = {
        "messaging_product": "whatsapp",
        "to": from_num,
        "recipient_type": "individual",
        "type": "interactive",
        "interactive": {
            "type": "button",
                "body": {
                    "text": "Please select the option to continue ahead"
                    },
                "action": {
                    "buttons": [
                        {
                            "type": 'reply',
                            "reply": {
                                "id": 501,
                                "title": "Our Services"
                                }
                        },
                        {
                            "type": 'reply',
                            "reply": {
                                "id": 136,
                                "title": "Contact to Us"
                                }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": 137,
                                "title": "FAQ"
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



def message_data(user_id, user_name, user_contact, message, date, bought_plan=None):

    with sql.connect("/home/Harsh159/chat_dir/test_database/my_data.db", timeout=0.01) as user:

        cursor = user.cursor()

        if bought_plan is not None:

            cursor.execute("INSERT INTO finance_data (user_id, user_name, user_contact, \
                            message_data, date, bought_plan) VALUES (?, ?, ?, ?, ?, ?)", (user_id, \
                            user_name, user_contact, message, date, bought_plan))

            user.commit()

        else:

            cursor.execute("INSERT INTO finance_data (user_id, user_name, user_contact, \
                            message_data, date) VALUES (?, ?, ?, ?, ?)", (user_id, \
                            user_name, user_contact, message, date))

            user.commit()





def user_registration(from_num):

    wa_bot.send_message(from_num,
                        'Welcome to SAUBHAGYAM Pvt. Ltd. It looks like you need to create an account to see all services.',
                        reply_markup=Inline_keyboard(['Create an account', 'Contact Saubhagyam']))



def main_menu(from_num):

    data = {
        "messaging_product": "whatsapp",
        "to": from_num,
        "recipient_type": "individual",
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header":{
                "type": "text",
                "text": "Main Menu"
                },
                "body": {
                    "text": "Please select the option"
                    },
                "action": {
                    "buttons": [
                        {
                            "type": 'reply',
                            "reply": {
                                "id": 501,
                                "title": "Our Services"
                                }
                        },
                        {
                            "type": 'reply',
                            "reply": {
                                "id": 136,
                                "title": "Contact to Us"
                                }
                        },
                        {
                            "type": 'reply',
                            "reply": {
                                "id": 137,
                                "title": "FAQ"
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



def list_message(id_message, user_contact):

    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    with sql.connect('/home/Harsh159/chat_dir/test_database/user_data.db', timeout=5) as user:

        cursor = user.cursor()

        cursor.execute('SELECT message_title FROM now_work WHERE message_id=?', (id_message,))

        main_message  = cursor.fetchone()


        cursor.execute('SELECT user_id, user_name, user_contact FROM \
                        finance_data WHERE user_contact=?', (user_contact,))

        user_data = cursor.fetchone()



        message_data(user_data[0], user_data[1], user_data[2], main_message[0], date, bought_plan='Yes')


        if main_message is not None:

            button_text_message(from_num=user_contact, text_body=f'Thank you for the response for {main_message[0]}. Our team will come to you in 3 hours.', \
                                button_id_1=501, title_1='Service Section', button_id_2=305, title_2='Main Menu')

        elif id_message == "305" or id_message == "809":
            return main_menu(wa_num)




def button_message(id_message, user_contact=None):

    if id_message == "501":
        return our_services(user_contact)

    elif id_message == "305" or id_message == "809":
        return main_menu(wa_num)




def interactive_message(message, user_contact):

    if message == "Our Services" or message == "Service Section":
        return our_services(user_contact)

    elif message == "Contact to Us":
        return button_text_message(from_num=user_contact, \
                                   text_body="You can contact us on this number 919456899889", \
                                   title_1="Service Section", button_id_1=501, button_id_2=305, \
                                   title_2="Main Menu")

    elif message == "Main Menu":
        return main_menu(user_contact)

    elif message == "FAQ":
        return faq_message(user_contact)




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



def faq_message(user_contact):

    text_message(user_contact, "All possible loan options are available online.")

    text_message(user_contact, "You can get money without any documents.")

    text_message(user_contact, "You can withdraw your money at a moment.")

    text_message(user_contact, "All the date of payment will be 15 of month.")

    text_message(user_contact, "You can check your profile at our website.")

    return button_text_message(from_num=user_contact, text_body="Please check for more answers at our website.", \
                               button_id_1=305, title_1="Service Section", button_id_2=809, title_2="Main Menu")





def button_text_message(from_num, text_body, button_id_1, title_1, button_id_2, title_2):

    data = {
        "messaging_product": "whatsapp",
        "to": from_num,
        "recipient_type": "individual",
        "type": "interactive",
        "interactive": {
            "type": "button",
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



def our_services(from_num):

    with sql.connect('/home/Harsh159/chat_dir/test_database/user_data.db', timeout=5) as user:

        cursor = user.cursor()

        cursor.execute('SELECT message_id, message_title, message_description FROM now_work')


        finance_data = cursor.fetchall()


        data = {
            "messaging_product": "whatsapp",
            "to": from_num,
            "recipient_type": "individual",
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": "Please select the option"
                    },
                "action": {
                    "button": "All Options",
                    "sections": [
                        {
                            "title": "All Options",
                            "rows": [{"id": finan_id, "title": finan_name, "description": finan_details} \
                                     for finan_id, finan_name, finan_details in finance_data]

                        }
                    ]
                }
            }
        }


    response = requests.post(url, json=data, headers=headers)
    print(f"Whatsapp message response :- {response.json}")
    response.raise_for_status()

    return response



def handle_whatsapp_message(body):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    user_name = body['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
    user_id = body['entry'][0]['id']
    user_contact_num = body['entry'][0]['changes'][0]['value']['messages'][0]['from']
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    if message["type"] == "interactive":


        # List reply response

        if message["interactive"]["type"] == "list_reply":

            id_message = message["interactive"]["list_reply"]["id"]
            # list_reply_message = message["interactive"]["list_reply"]["title"]

            # message_data(user_name, list_reply_message, user_contact_num, user_id)

            return list_message(id_message, wa_num)



        # Button reply response

        elif message["interactive"]["type"] == "button_reply":

            message_body = message["interactive"]["button_reply"]["title"]
            id_message = message["interactive"]["button_reply"]["id"]

            message_data(user_id, user_name, user_contact_num, message_body, date)

            if message_body == 'Our Services':

                return interactive_message(message_body, user_contact_num)

            elif message_body == 'Contact to Us':

                return interactive_message(message_body, user_contact_num)

            elif message_body == 'FAQ':

                return interactive_message(message_body, user_contact_num)

            else:

                return button_message(id_message, user_contact_num)



    # Order Message

    elif message["type"] == "order":

        product_items = body["entry"][0]["changes"][0]["value"]\
                        ["messages"][0]["order"]["product_items"]

        with sql.connect('/home/Harsh159/chat_dir/test_database/user_data.db', timeout=5) as user:

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


        # payment_method(user_contact_num)




    elif message["type"] == "text":
        message_body = message["text"]["body"].lower()
        # We can convert in uppercase or in high.


        start_messages = ["hey", "hi", "hello"]


        if any([a in message_body for a in start_messages]):

            with sql.connect('/home/Harsh159/chat_dir/user_data.db', timeout=5) as user:
                cursor = user.cursor()

                cursor.execute('SELECT * FROM registered_users WHERE user_contact=?', (user_contact_num,))

                data = cursor.fetchone()

                if data is None:
                    message_data(user_id, user_name, user_contact_num, message_body, date)
                    return user_registration(user_contact_num)

                else:
                    message_data(user_id, user_name, user_contact_num, message_body, date)
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
