import razorpay
man = razorpay.Client(auth=("rzp_test_lrU6iwIvDYnbOO", "DsehDWPamICKR7VUJrTQ8PqN"))

new_one = man.payment_link.create({
  "amount": 500*100,
  "currency": "INR",
  "accept_partial": True,
  "first_min_partial_amount": 100,
  "description": "For XYZ purpose",
  "customer": {
    "name": "Gaurav Kumar",
    "email": "gaurav.kumar@example.com",
    "contact": "+919000090000"
  },
  "notify": {
    "sms": True,
    "email": True
  },
  "reminder_enable": True,
  "notes": {
    "address": "09, Shree prabhu park society, Naroda, Ahmedabad",
    "whatsapp_num": 919312345619
  }
})


print(new_one)



'''import json
import os
import stripe
from flask import Flask, jsonify, request

stripe.api_key = "sk_test_51NvaaxSEkU2J3j1RdZrON2yDXecUzcowPoroYM6qB5Nq44x9BE6quYHJ62SlqRsVY5HNllUO7C6kvJgRSbOOnknC00ZW1703ui"

endpoint_secret = 'whsec_6bad48d6a0090800970b54bfdb25568ef41e9cee526c54f2960ef8c497fd9fd6'

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    event = None
    
    if request.method == 'GET':
       print('New one')
    
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        print(event)
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'payment_intended.succeeded':
      payout = event['data']['object']

      print(payout)
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)



if __name__ == '__main__':
   app.run(port=9003, debug=True)'''
