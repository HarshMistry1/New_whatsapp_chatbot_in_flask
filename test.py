from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

new_path = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(new_path, 'db.sqlite3')
SQLALCHEMY_BINDS = {
    'new': 'sqlite:///' + os.path.join(new_path, 'new_data.sqlite3')
}

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class RemoteUser(db.Model):
    __bind_key__ = 'new'
    id = db.Column(db.Integer, primary_key=True)

print(db.get_engine(app))  # will show sqlite db2.db
print(db.get_tables_for_bind('new'))  # will show remote_user table
# print(db.get_binds(app))


'''import stripe
stripe.api_key = "sk_test_51NvaaxSEkU2J3j1RdZrON2yDXecUzcowPoroYM6qB5Nq44x9BE6quYHJ62SlqRsVY5HNllUO7C6kvJgRSbOOnknC00ZW1703ui"

product_create = stripe.Product.create(name="Brush")
product_num = product_create.get('id')

price_create = stripe.Price.create(
  unit_amount=599*100,
  currency="inr",
  product=product_num
)

price_num = price_create.get('id')'''

# man = stripe.checkout.Session.create(
  # cancel_url="https://example.com",
  # line_items=[{"price": f'{price_num}', "quantity": 1}],
  # mode="payment",
  # success_url="https://example.com",
  # payment_method_types=["card", "link"]
# )



# new_link = stripe.PaymentLink.create(line_items=[{"price": f'{price_num}', "quantity": 1}])

# print(new_link)








'''import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
import json
import os

max_len = 25

path = '/home/saubhagyam/Downloads/my_new_project/'

with open(path + 'new_intents.json', 'r') as f:
  data = json.loads(f.read())

tokeniser_path = open(path + 'tokenizer.pkl', 'rb')
tokeniser = pickle.load(tokeniser_path)
label_path = open(path + 'label_encoder.pkl', 'rb')
label_enc = pickle.load(label_path)

model = tf.keras.models.load_model(path + 'new_chatbot_model.h5')

res = model.predict(pad_sequences(tokeniser.texts_to_sequences(['bye']),
                                  truncating='post', maxlen=max_len))

tag_out = label_enc.inverse_transform([np.argmax(res)])

for p in data['intents']:
  if p['tag'] == tag_out:
    print(np.random.choice(p['responses']))'''

'''import sqlite3 as sql



def message_data(data, messa_type=None, database_value=None):

    with sql.connect('/home/saubhagyam/Downloads/user_data.db') as user:

        cursor = user.cursor()

        if messa_type == 'update_data':

            cursor.execute(data, database_value)
            user.commit()

        else:
            cursor.execute(data)
            data = cursor.fetchall()
            
            return data
    


user_messa_search = 'Harsh'
# data = message_data(data=f"UPDATE message_data SET delivery_status='Delivered' WHERE order_id=?", \
                    # messa_type='update_data', database_value=('5AF659',))

data = message_data(f"SELECT user_name, delivery_status, time_of_message, user_contact FROM \
                    message_data WHERE user_name LIKE '%{user_messa_search}%' OR delivery_status LIKE \
                    '%{user_messa_search}%' OR time_of_message LIKE '%{user_messa_search}%' OR \
                    user_contact LIKE '%{user_messa_search}%' GROUP BY user_name LIMIT 10")

print(data)'''


# data = sql.connect('/home/Harsh159/chat_dir/user_data.db')
# data.execute('CREATE TABLE IF NOT EXISTS registered_users (\
              # id INTEGER PRIMARY KEY AUTOINCREMENT, \
              # user_name TEXT NOT NULL, \
              # user_contact INTEGER NOT NULL \
              # )')'

# link = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Sydney_Australia._%2821339175489%29.jpg/250px-Sydney_Australia._%2821339175489%29.jpg'
# date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# print(os.getenv('ASSETS_ROOT', '/home/Harsh159/chat_dir/static/assets/'))


# with sql.connect('/home/Harsh159/chat_dir/test_database/my_data.db') as user:
    # cursor = user.cursor()
    # cursor.execute('INSERT INTO registered_users (user_name, user_contact) VALUES (?, ?)', ('Virang Patel', 919998978397))
    # cursor.execute('INSERT INTO cart_list (user_name, user_contact, product_name, \
                    # product_id, quantity, price, link, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    # ('Harsh Mistry', 919662104238, 'Australia', 407, 1, 69000, link, date))
    # cursor.execute('CREATE TABLE IF NOT EXISTS main_product_list (\
                       # id INTEGER PRIMARY KEY AUTOINCREMENT, \
                       # product_id TEXT NOT NULL, \
                       # product_name TEXT NOT NULL, \
                       # price INTEGER NOT NULL)')

    # cursor.execute('CREATE TABLE IF NOT EXISTS main_cart_list (\
                    # id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    # product_id TEXT NOT NULL, \
                    # product_name TEXT NOT NULL, \
                    # user_name TEXT NOT NULL, \
                    # user_contact INTEGER NOT NULL, \
                    # quantity INTEGER NOT NULL, \
                    # price INTEGER NOT NULL, \
                    # date TIMESTAMP NOT NULL)')'''

    # cursor.execute('CREATE TABLE IF NOT EXISTS all_customer_shop( \
                    # id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    # user_name TEXT NOT NULL, \
                    # user_contact INTEGER NOT NULL, \
                    # product_name TEXT NOT NULL, \
                    # quantity INTEGER NOT NULL, \
                    # price INTEGER NOT NULL, \
                    # payment_method TEXT NOT NULL, \
                    # date TIMESTAMP NOT NULL)')'''

    # cursor.execute('CREATE TABLE IF NOT EXISTS finance_data( \
                    # id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    # user_id INTEGER NOT NULL, \
                    # user_name TEXT NOT NULL, \
                    # user_contact INTEGER NOT NULL, \
                    # message_data TEXT NOT NULL, \
                    # bought_plan TEXT NOT NULL DEFAULT No, \
                    # date TIMESTAMP NOT NULL)')


    # cursor.execute('INSERT INTO registered_users (user_name, contact_user) \
                    # VALUES (?, ?)', ('Mihir Soni', 919428398825))


    # cursor.execute('CREATE TABLE IF NOT EXISTS new_product_list (\
                    # id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    # product_id TEXT NOT NULL, \
                    # product_name TEXT NOT NULL, \
                    # product_categ_id INTEGER NOT NULL, \
                    # price INTEGER NOT NULL)')

    # cursor.execute('SELECT * FROM registered_users')

    # cursor.execute('SELECT * FROM new_product_list')


    # cursor.execute('INSERT INTO new_product_list (product_id, \
                    # product_name, product_categ_id, price) \
                    # VALUES (?, ?, ?, ?)', ('gsww3p85lv', \
                    # 'Blue T-Shirt for Men', 5, 501))

    # cursor.execute('INSERT INTO now_work (message_id, \
                    # message_title, message_description) \
                    # VALUES (?, ?, ?)', (128, 'Data Work', \
                    # 'We work on data as per your need.'))


    # cursor.execute('SELECT * FROM main_product_list')

    # cursor.execute('CREATE TABLE IF NOT EXISTS file_management (\
                    # id INTEGER DEFAULT 101, \
                    # user_name TEXT NOT NULL, \
                    # user_contact INTEGER NOT NULL, \
                    # billno INTEGER PRIMARY KEY AUTOINCREMENT, \
                    # file_name TEXT NOT NULL, \
                    # date TIMESTAMP NOT NULL)')'''


    # cursor.execute('DELETE FROM registered_users WHERE id=?', (4,))


    # cursor.execute('CREATE TABLE IF NOT EXISTS now_work (\
                    # id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    # message_id INTEGER NOT NULL, \
                    # message_title TEXT NOT NULL, \
                    # message_description TEXT NOT NULL)')



    # cursor.execute('CREATE TABLE IF NOT EXISTS finance_work (\
                    # id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    # finance_id INTEGER NOT NULL, \
                    # finance_name TEXT NOT NULL, \
                    # finance_description TEXT NOT NULL)')


    # cursor.execute('INSERT INTO finance_work \
                   # (finance_id, finance_name, \
                   # finance_description) VALUES \
                   # (?, ?, ?)', (107, \
                   # 'Cash Credit', \
                   # 'In this one you can get cash in your account))




    # cursor.execute('DELETE FROM file_management')

    # cursor.execute('SELECT * FROM main_product_list')

    # cursor.execute('DELETE FROM new_product_list')





    # cursor.execute('INSERT INTO customer_complaints (complaint, \
                    # complaint_id, details) VALUES (?, ?, ?)', \
                    # ('New Products', 319, 'Let us know about new products.'))'''


    # cursor.execute('INSERT INTO main_product_list (product_id, product_name, \
                    # price, product_categ_id) VALUES (?, ?, ?, ?)', \
                    # ('qncco293g6', 'New White for Men', 501, 2))'''


    # cursor.execute('UPDATE new_product_list SET price=? WHERE id=?', \
                  # (301, 6))

    # cursor.execute('UPDATE finance_work SET finance_description=? WHERE id=?', \
                   # ('In start up loan we provide you the start up loan', 6))


    # cursor.execute('UPDATE customer_complaints SET complaint=? WHERE id=?', ('My Order', 4,))

    # cursor.execute('SELECT * FROM main_cart_list')

    # cursor.execute('SELECT * FROM all_customer_shop')

    # cursor.execute('DELETE FROM customer_complaints WHERE id=?', (7,))

    # cursor.execute('SELECT product_id FROM main_product_list WHERE product_categ_id=?', (2,))

    # cursor.execute('ALTER TABLE main_product_list ADD product_categ_id INTEGER')

    # cursor.execute('SELECT SUM(quantity*price) as new_price FROM main_cart_list WHERE \
                    # user_contact=?', (919662104238,))

    # cursor.execute('DELETE FROM main_product_list WHERE id=?', (8,))

    # cursor.execute('DELETE FROM cart_list')
    # user.commit()

    # cursor.execute('SELECT * FROM main_product_list')

    # my_data = cursor.fetchall()

    # print(my_data)


    # if my_data is not None:
        # print('You have the data.')

    # else:
        # print('Check the data.')'''










# import datetime

# now  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# print(now)







































