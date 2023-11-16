import json
from flask import Flask, request
from flask.json import jsonify
import requests
from python_whatsapp_bot import Whatsapp

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





def send_interactive_message(from_num, message_type, text_body, header=None, header_text=None, file_name=None, link=None, button_messages=None, list_data=None):
    my_data = request.get_json()
    user_name = my_data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']

    text_message(from_num, f"Hello {user_name}.")

    text_message(from_num, "Welcome to Saubhagyam Web Pvt. Ltd.")


    data = {
        "messaging_product": "whatsapp",
        "to": from_num,
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
                                "id": 135,
                                "title": "Looking for Services"
                                }
                        },
                        {
                            "type": 'reply',
                            "reply": {
                                "id": 136,
                                "title": "Contact Saubhagyam"
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

    from_num = user_contact

    if id_message == "501":
        text_message(user_contact, 'We develop mobile application.')

    elif id_message == "502":
        text_message(user_contact, 'We develop we application.')

    elif id_message == "503":
        text_message(user_contact, 'We develop prediction model.')

    elif id_message == "504":
        button_text_message(user_contact=from_num, text_body='Thank you for choosing chatbot development. Please select', \
                            button_id_1=101, title_1='Button Type', button_id_2=104, title_2='Conversational Type')

    elif id_message == "505":
        text_message(from_num, 'We have a service on digital marketing.')




def button_message(id_message, from_num=None):


    if id_message == "359":
        return service_message(from_num)

    elif id_message == "305" or id_message == "809":
        return main_menu(wa_num)




def interactive_message(message, from_num):

    if message == "Looking for Services":
        return service_message(from_num)

    if message == "Button Type":
        text_message(from_num, 'Thank you for choosing our chatbot services')
        button_text_message(user_contact=from_num, text_body='Our team will contact you for further information about chatbot', \
                            button_id_1=359, title_1='Service Section', button_id_2=305, title_2='Main Menu')

    elif message == "Conversational Type":
        text_message(from_num, 'Thank you for choosing our chatbot services')
        button_text_message(user_contact=from_num, text_body='Our team will contact you for further information about chatbot', \
                            button_id_1=359, title_1='Service Section', button_id_2=305, title_2='Main Menu')

    elif message == "Main Menu":
        return main_menu(from_num)





def button_text_message(user_contact, text_body, button_id_1, title_1, button_id_2, title_2):

    data = {
        "messaging_product": "whatsapp",
        "to": user_contact,
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



def service_message(from_num):

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
                            "rows": [
                                {
                                    "id": 501,
                                    "title": 'Mobile App Development',
                                    "description": 'We develop mobile application as customer requirement.'
                                },
                                {
                                    "id": 502,
                                    "title": 'Web Development',
                                    "description": 'We develop web application as customer need.'
                                },
                                {
                                    "id": 503,
                                    "title": 'AI/ML Development',
                                    "description": 'We develop models for prediction as customer wants.'
                                },
                                {
                                    "id": 504,
                                    "title": 'Chatbot Development',
                                    "description": 'We develop chatbot for website yet for whatsapp business.'
                                },
                                {
                                    "id": 505,
                                    "title":'Digital Marketing',
                                    "description": 'We have a service of digital marketing.'
                                }


                            ]

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
    user_contact_num = body['entry'][0]['changes'][0]['value']['messages'][0]['from']


    if message["type"] == "interactive":


        # List reply response

        if message["interactive"]["type"] == "list_reply":

            id_message = message["interactive"]["list_reply"]["id"]

            return list_message(id_message, wa_num)



        # Button reply response

        elif message["interactive"]["type"] == "button_reply":

            message_body = message["interactive"]["button_reply"]["title"]
            id_message = message["interactive"]["button_reply"]["id"]



            if message_body == 'Looking for Services':

                return interactive_message(message_body, user_contact_num)


            elif message_body == 'Online Payment':

                return interactive_message(message_body, from_num=user_contact_num)


            elif message_body == 'Button Type':

                return interactive_message(message_body, from_num=user_contact_num)


            elif message_body == 'Conversational Type':

                return interactive_message(message_body, from_num=user_contact_num)


            elif message_body == 'Contact Saubhagyam':

                return interactive_message(message_body, from_num=user_contact_num)


            else:

                return button_message(id_message, user_contact_num)




    elif message["type"] == "text":
        message_body = message["text"]["body"].lower()
        # We can convert in uppercase or in high.

        start_messages = ["hey", "hi", "hello"]

        if any([a in message_body for a in start_messages]):

            send_interactive_message(from_num=wa_num, message_type='button', \
                                     text_body='Please, select the option to go ahead', \
                                     button_messages=[(135, 'Looking for Services'), \
                                     (136, 'Contact Saubhagyam')])

        else:

            return text_message(user_contact_num, "Please start conversation with 'Hello'.")






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
